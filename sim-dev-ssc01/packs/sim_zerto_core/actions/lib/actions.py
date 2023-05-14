import ssl
import requests
import json
from st2common.runners.base_action import Action

CONNECTION_ITEMS = ['host', 'port']


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        if config is None:
            raise ValueError("No connection configuration details found")
        if "zerto" in config:
            if config['zerto'] is None:
                raise ValueError("'zerto' config defined but empty.")
            else:
                pass
        else:
            raise ValueError("No connection configuration details found")

        self.ssl_verify = config['zerto'].get('ssl_verify', None)
        self.authorization = config['zerto'].get('authorization')
        if self.ssl_verify is False:
            # Don't print out ssl warnings
            requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context

    def establish_connection(self, zerto, port):
        """
        Sets:
        - access_token
        """
        response = self._connect(zerto, port)
        status_code = response.status_code

        if status_code >= 200 and status_code <= 299:
            access_token = response.headers['x-zerto-session']
        else:
            raise Exception(response.headers)

        return access_token


    def _connect(self, zerto, port):
        try:
            endpoint = "https://{}:{}/v1/session/Add".format(zerto, port)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.authorization
            }
            session = requests.Session()
            response = session.post(url=endpoint, headers=headers, verify=self.ssl_verify)
            response.raise_for_status()
            return response
        except Exception as e:
            raise Exception(e)
