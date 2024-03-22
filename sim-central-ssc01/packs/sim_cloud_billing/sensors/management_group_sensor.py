from st2reactor.sensor.base import PollingSensor
import sqlalchemy
from sqlalchemy.engine.url import URL
import decimal
import datetime
from contextlib import contextmanager
import uuid
import pytz
from operator import itemgetter
from itertools import groupby
batch_size = 100

#                         (key, required, default)
CONFIG_CONNECTION_KEYS = [('host', False, ""),
                          ('username', False, ""),
                          ('password', False, ""),
                          ('database', True, ""),
                          ('port', False, None),
                          ('drivername', True, "")]

DEFAULT_KNOWN_DRIVER_CONNECTORS = {
    'postgresql': 'postgresql+psycopg2',
    'mysql': 'mysql+pymysql',
    'oracle': 'oracle+cx_oracle',
    'mssql': 'mssql+pymssql',
    'firebird': 'firebird+fdb'
}

CONN = 'cloudmanagement'

class ManagementGroupSensor(PollingSensor):
    def __init__(self, config, sensor_service, poll_interval=300):
        super(ManagementGroupSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self.trigger_name = 'management_group'
        self.trigger_pack = 'sim_cloud_billing'
        self.trigger_ref = '.'.join([self.trigger_pack, self.trigger_name])
        self._poll_interval = poll_interval
        self.payload = []
        self.conn_obj = {}

    def setup(self):
        self.conn_obj = {'connection': CONN}
        self._logger.debug('Setting up GroupHandlerSensor ...')

    def poll(self):
        self._logger.debug('Running GroupHandlerSensor ...')
        self.conn_obj = {'connection': CONN}
        self._detect_schedules()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _detect_schedules(self):
        current_utc_ts = datetime.datetime.now()
        current_ast_ts = current_utc_ts.astimezone(pytz.timezone('Australia/Sydney'))
        current_day    = current_ast_ts.strftime('%A')
        current_hour   = current_ast_ts.strftime('%H')
        current_minute = self.closest_left(int(current_ast_ts.strftime('%M')))
        #current_time   = '{:02d}:{:02d}'.format(current_hour, current_minute)
        #if current_minute < 10:
        #    current_time = '{}:0{}'.format(current_hour, current_minute)
        #else:
        #    current_time = '{}:{}'.format(current_hour, current_minute)
        current_time = '{}:{}'.format(current_hour, current_minute)
        self.current_day  = current_day
        self.current_time = current_time
        return_result = None
        with self.db_connection(self.conn_obj) as conn:
            # Execute the query
            COUNT_QUERY = f"""
                          SELECT COUNT(*) AS Count
                          From IaaS_ManagementGroupMember a,
                          IaaS_Live b,
                          IaaS_ManagementGroupSchedule c,
                          IaaS_ManagementGroup d
                          where a.managedID=b.managedID
                          and d.GroupStatus = 'Enabled'
                          and a.ManagmentGroupSIName = c.ManagementGroupSIName
                          and a.ManagmentGroupSIName = d.Name
                          and c.Day='{self.current_day}'
                          and CONVERT(time, c.ActionTime) = CONVERT(time, '{self.current_time}')
                          and (
                            (b.managedBy = 'vcenter' AND b.vmActive = '1')
                            OR
                            (b.managedBy <> 'vcenter')
                          )
                          """
            self._logger.debug(COUNT_QUERY)
            rows = conn.execute(COUNT_QUERY).fetchone()

            for start_row in range(0, rows['Count'], batch_size):
                QUERY = f"""
                        SELECT *
                        FROM (SELECT ROW_NUMBER() OVER (ORDER BY a.StartupSequence ASC) AS RowNumber, a.ServerFriendlyName,
                            c.Action,
                            a.managedID,
                            a.Name,
                            b.vmID,
                            a.StartupDelay,
                            a.StartupSequence,
                            a.ShutdownDelay,
                            a.ManagmentGroupSIName,
                            b.vmGuestToolsStatus,
                            b.managedBy,
                            b.managedByID
                            From IaaS_ManagementGroupMember a,
                            IaaS_Live b,
                            IaaS_ManagementGroupSchedule c,
                            IaaS_ManagementGroup d
                            where a.managedID=b.managedID
                            and d.GroupStatus = 'Enabled'
                            and a.ManagmentGroupSIName = c.ManagementGroupSIName
                            and a.ManagmentGroupSIName = d.Name
                            and c.Day='{self.current_day}' 
                            and CONVERT(time, c.ActionTime) = CONVERT(time, '{self.current_time}')
                            and (
                                (b.managedBy = 'vcenter' AND b.vmActive = '1')
                                OR
                                (b.managedBy <> 'vcenter')
                            )) AS RowNumberedTable
                        WHERE RowNumber BETWEEN {start_row + 1} AND {start_row + batch_size}
                        """
                self._logger.debug(QUERY)
                query_result = conn.execute(QUERY)

                # We need to execute these commands while connection is still open.
                return_result = {'affected_rows': query_result.rowcount}
                if query_result.returns_rows:
                    return_result = []
                    all_results = query_result.fetchall()
                    for row in all_results:
                        self._logger.info('Processing ManagementGroup: {}, VM: {}'.format(row['ManagmentGroupSIName'], row['ServerFriendlyName']))
                        return_result.append(self.row_to_dict(row))
                if len(return_result) > 0:
                    self._logger.info('Records found: {}'.format(len(return_result)))
                    '''
                    groups = {}
                    for item in return_result:
                        group_key = (item['StartupSequence'], item['Action'], item['managedByID'])
                        identifier = self.identifier_func(item)
                        if group_key not in groups:
                            groups[group_key] = {'identifier': identifier, 'items': []}
                        groups[group_key]['items'].append(item)
                    '''
                    self._dispatch_trigger(return_result)

    def identifier_func(self, group):
        return f"{group['StartupSequence']}_{group['Action']}_{group['managedByID']}"

    def closest_left(self, K):
        lst = [0,5,10,15,20,25,30,35,40,45,50,55]
        return max([i for i in lst if K >= i])

    def _dispatch_trigger(self, groups):
        trigger = self.trigger_ref
        payload = {}
        payload['trigger_payload'] = groups
        trace_tag = uuid.uuid4().hex
        self.sensor_service.dispatch(trigger=trigger, payload=payload, trace_tag=trace_tag)


    def get_del_arg(self, key, kwargs_dict, delete=False):
        """Attempts to retrieve an argument from kwargs with key.
        If the key is found, then delete it from the dict.
        :param key: the key of the argument to retrieve from kwargs
        :returns: The value of key in kwargs, if it exists, otherwise None
        """
        if key in kwargs_dict:
            value = kwargs_dict[key]
            if delete:
                del kwargs_dict[key]
            return value
        else:
            return None

    def row_to_dict(self, row):
        """When SQLAlchemy returns information from a query the rows are
        tuples and have some data types that need to be converted before
        being returned.
        returns: dictionary of values
        """
        return_dict = {}
        for column in row.keys():
            value = getattr(row, column)

            if isinstance(value, datetime.date):
                return_dict[column] = value.isoformat()
            elif isinstance(value, decimal.Decimal):
                return_dict[column] = float(value)
            else:
                return_dict[column] = value

        return return_dict

    @contextmanager
    def db_connection(self, kwargs_dict):
        """Connect to the database and instantiate necessary methods to be used
        later.
        """
        # Get the connection details from either config or from action params
        connection = self.resolve_connection(kwargs_dict)

        # Update Driver with a connector
        default_driver = DEFAULT_KNOWN_DRIVER_CONNECTORS.get(connection['drivername'], None)
        if default_driver:
            connection['drivername'] = default_driver

        # Format the connection string
        database_connection_string = URL(**connection)

        self.engine = sqlalchemy.create_engine(database_connection_string, echo=False)
        self.meta = sqlalchemy.MetaData()
        conn = self.engine.connect()

        try:
            yield conn
        finally:
            conn.close()

    def validate_connection(self, connection, connection_name):
        """Ensures that all required parameters are in the connection. If a
        required parameter is missing a KeyError exception is raised.
        :param connection: connection to validate
        :returns: True if the connection is valid
        """
        for key, required, default in CONFIG_CONNECTION_KEYS:
            # ensure the key is present in the connection?
            if key in connection and connection[key]:
                continue

            # skip if this key is not required
            if not required:
                continue

            if connection_name:
                raise KeyError("config.yaml mising: sql:{0}:{1}"
                               .format(connection_name, key))
            else:
                raise KeyError("Because the 'connection' action parameter was"
                               " not specified, the following action parameter"
                               " is required: {0}".format(key))
        return True

    def resolve_connection(self, kwargs_dict):
        """Attempts to resolve the connection information by looking up information
        from action input parameters (highest priority) or from the config (fallback).
        :param kwargs_dict: dictionary of kwargs containing the action's input
        parameters
        :returns: a dictionary with the connection parameters (see: CONFIG_CONNECTION_KEYS)
        resolved.
        """
        connection_name = self.get_del_arg('connection', kwargs_dict, True)
        config_connection = None
        if connection_name:
            config_connection = self.config['connections'].get(connection_name)
            if not config_connection:
                raise KeyError("config.yaml missing connection: sql:{0}"
                               .format(connection_name))

        action_connection = {}

        # Override the keys in creds read in from the config given the
        # override parameters from the action itself
        # Example:
        #   'username' parameter on the action will override the username
        #   from the credential. This is useful for runnning the action
        #   standalone and/or from the commandline
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if key in kwargs_dict and kwargs_dict[key]:
                # use params from cmdline first (override)
                action_connection[key] = self.get_del_arg(key, kwargs_dict)
            elif config_connection and key in config_connection and config_connection[key]:
                # fallback to creds in config
                action_connection[key] = config_connection[key]
            else:
                if not required and default:
                    action_connection[key] = default

            # remove the key from kwargs if it's still in there
            if key in kwargs_dict:
                del kwargs_dict[key]
            

        self.validate_connection(action_connection, connection_name)

        return action_connection

    def closest(self, K):
        lst = [0,15,30,45]
        return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
