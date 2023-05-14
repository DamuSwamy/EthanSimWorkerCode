import json
from lib.actions import BaseAction
from lib import zerto_api

class ZCMGetSitesAction(BaseAction):
    def run(self, zerto, port=443, access_token=None):
        ret = False
        args = {}
        if access_token is None:
            access_token = self.establish_connection(zerto, port)

        args['access_token'] = access_token
        
        args['url'] = "https://{}:{}/v1/sites".format(zerto, port)
        args['method'] = "get"

        req_data = zerto_api.addArgs(**args)
        resp = zerto_api.makeRequest(**req_data)

        myresp = {}
        myresp['status_code'] = resp.status_code
        try:
            myresp['data'] = json.loads(resp.content.rstrip())
        except ValueError:
            myresp['data'] = resp.content

        result = []
        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True
            for site in myresp['data']:
                site_obj = {"zvmSiteName": site['SiteName'],
                            "zvmHostName": site['HostName'],
                            "zvmSiteType": site['CloudSiteType'],
                            "zvmIdentity": site['SiteIdentifier'],
                            "zvmSiteSession": site['ZvmGui']['SessionIdentifier'],
                            "zvmVersion": site['ZvmVersion']}
                result.append(site_obj)

        return (ret, result)
