import ssl
import requests
import json
from st2common.runners.base_action import Action

CONNECTION_ITEMS = ['host', 'user', 'passwd']


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        if config is None:
            raise ValueError("No connection configuration details found")
        if "braas" in config:
            if config['braas'] is None:
                raise ValueError("'braas' config defined but empty.")
            else:
                pass
        else:
            raise ValueError("No connection configuration details found")

        self.ssl_verify = config.get('ssl_verify', None)
        if self.ssl_verify is False:
            # Don't print out ssl warnings
            requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context

    def establish_connection(self, braas):
        """
        Sets:
        - access_token
        """
        response = self._connect(braas)
        status_code = response.status_code
        try:
            data = json.loads(response.content.rstrip())
        except ValueError:
            data = response.content

        if status_code >= 200 and status_code <= 299:
            access_token = data['access_token']
        else:
            raise Exception(data)

        return access_token



    def _get_connection_info(self, braas):
        if braas:
            connection = self.config['braas'].get(braas)
        else:
            connection = self.config['braas'].get('default')

        for item in CONNECTION_ITEMS:
            if item in connection:
                pass
            else:
                raise KeyError("sim_braas.yaml Mising: braas:%s:%s"
                               % (braas, item))

        return connection

    def _connect(self, braas):
        connection = self._get_connection_info(braas)

        try:
            endpoint = "https://{}/api/v1/oauth/swagger".format(connection['host'])
            params   = {"grant_type": "password",
                        "username": connection['user'],
                        "password": connection['passwd']}
            
            headers = {
                'Content-Type': 'application/json',
            }
            s = requests.Session()
            return getattr(s, 'post')(url=endpoint, headers=headers, params=params, verify=self.ssl_verify)
        except Exception as e:
            raise Exception(e)
