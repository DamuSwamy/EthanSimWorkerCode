from lib.base_action import BaseAction
import sqlalchemy
from sqlalchemy.sql.expression import bindparam


class SQLBulkUpdateAction(BaseAction):
    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(SQLBulkUpdateAction, self).__init__(config)

    def run(self, **kwargs):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: the dns adapters and the number of network adapters to be
        on the VM.
        """
        kwargs_dict = dict(kwargs)

        update_dict = self.get_del_arg('data', kwargs_dict)
        table = self.get_del_arg('table', kwargs_dict)
        column_filter1 = self.get_del_arg('column_filter1', kwargs_dict)
        column_filter2 = self.get_del_arg('column_filter2', kwargs_dict)
        column_filter3 = self.get_del_arg('column_filter3', kwargs_dict)
        column_filter4 = self.get_del_arg('column_filter4', kwargs_dict)
        column_filter5 = self.get_del_arg('column_filter5', kwargs_dict)
        update_values  = self.get_del_arg('update_values', kwargs_dict)

        with self.db_connection(kwargs_dict) as conn:
            # Get the SQL table
            sql_table = sqlalchemy.Table(table,
                                        self.meta,
                                        autoload=True,
                                        autoload_with=self.engine)

            result = {}
            for value in update_values:
                result[value] = bindparam('{}'.format(value))
            print(result)

            if column_filter1:
                stmt = sql_table.update().where(sql_table.c.get(column_filter1) == bindparam('_{}'.format(column_filter1))).values(result)

            if column_filter1 and column_filter2:
                stmt = sql_table.update().where(sql_table.c.get(column_filter1) == bindparam('_{}'.format(column_filter1)), sql_table.c.get(column_filter2) == bindparam('_{}'.format(column_filter2))).values(result)
            if column_filter1 and column_filter2 and column_filter3:
                stmt = sql_table.update().where(sql_table.c.get(column_filter1) == bindparam('_{}'.format(column_filter1)), sql_table.c.get(column_filter2) == bindparam('_{}'.format(column_filter2)), sql_table.c.get(column_filter3) == bindparam('_{}'.format(column_filter3))).values(result)

            if column_filter1 and column_filter2 and column_filter3 and column_filter4:
                stmt = sql_table.update().where(sql_table.c.get(column_filter1) == bindparam('_{}'.format(column_filter1)), sql_table.c.get(column_filter2) == bindparam('_{}'.format(column_filter2)), sql_table.c.get(column_filter3) == bindparam('_{}'.format(column_filter3)), sql_table.c.get(column_filter4) == bindparam('_{}'.format(column_filter4))).values(result)

            if column_filter1 and column_filter2 and column_filter3 and column_filter4 and column_filter5:
                stmt = sql_table.update().where(sql_table.c.get(column_filter1) == bindparam('_{}'.format(column_filter1)), sql_table.c.get(column_filter2) == bindparam('_{}'.format(column_filter2)), sql_table.c.get(column_filter3) == bindparam('_{}'.format(column_filter3)), sql_table.c.get(column_filter4) == bindparam('_{}'.format(column_filter4)), sql_table.c.get(column_filter5) == bindparam('_{}'.format(column_filter5))).values(result)
            print(stmt)

            result = conn.execute(stmt, update_dict)

        return {'affected_rows': result.rowcount}
