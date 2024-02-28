import ssl
import requests
import json
from st2common.runners.base_action import Action

CONNECTION_ITEMS = ['cluster', 'authorization']

class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        if config is None:
            raise ValueError("No connection configuration details found")
        if "fsaas" in config:
            if config['fsaas']['vb4-isi1'] is None:
                raise ValueError("'vb3-isi1' config defined but empty.")
            else:
                pass
        else:
            raise ValueError("No connection configuration details found")

        self.ssl_verify = config['ssl_verify']
        self.authorization = config['fsaas'].get('vb4-isi1').get('authorization')
        if self.ssl_verify is False:
            # Don't print out ssl warnings
            requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context
