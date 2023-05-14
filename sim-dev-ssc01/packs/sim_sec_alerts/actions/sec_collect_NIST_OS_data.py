from st2common.runners.base_action import Action
import datetime
import json
import requests

class ReturnAssetVulDetails(Action):
    def run(self, asset, existing, **kwargs):
        asset_json = json.loads(asset)
        assets_cve = []
        print(asset_json)
        self.base_uri = 'https://services.nvd.nist.gov/rest/json/cves/1.0'
        endpoint = '{}?cpeMatchString={}&addOns=dictionaryCpes&apiKey=bbae5b04-84e6-4774-8e64-20094a6e6e73'.format(self.base_uri,asset_json['cpeID'])
        headers = {
                'Content-Type': 'application/json'
        }
        response = requests.request('get', endpoint, headers=headers, data={})
        print("Endpoint: "+ endpoint + ", status_code: "+ str(response.status_code))
        response_json = response.json()
        for cve in response_json['result']['CVE_Items']:
#           print("cve: "+ str(cve['cve']['CVE_data_meta']['ID']))
            asset_cve = {}
            asset_cve['id']                    = cve['cve']['CVE_data_meta']['ID']+ '|' +asset_json['cpeID']
            asset_cve['AssetID']               = asset_json['AssetID']
            asset_cve['cve']                   = cve['cve']['CVE_data_meta']['ID']
            asset_cve['cpeID']                 = asset_json['cpeID']
            asset_cve['vendor']                = asset_json['MatchingVendor']
            asset_cve['model']                 = asset_json['MatchingModel']
            asset_cve['osType']                = asset_json['MatchingOSType']
            asset_cve['osVersion']             = asset_json['MatchingOSVersion']
            asset_cve['netDBModel']            = asset_json['Model']
            asset_cve['impactBaseScore']       = cve['impact']['baseMetricV3']['cvssV3']['baseScore']
            asset_cve['impactBaseSeverity']    = cve['impact']['baseMetricV3']['cvssV3']['baseSeverity']
            for config in cve['configurations']['nodes']:
                if config['operator'] == 'AND':
#                   print (len([x for x in config['children'][0]['cpe_match'] if str(asset_cve['osType']) in x['cpe23Uri'] and str(asset_cve['osVersion']) in x['cpe23Uri']]))
                    if ((len([x for x in config['children'][0]['cpe_match'] if str(asset_cve['osType']) in x['cpe23Uri'] and str(asset_cve['osVersion']) in x['cpe23Uri']]) > 0) or (len([y for y in config['children'][0]['cpe_match'] if str(asset_cve['osType']+':*:*:*:*:*:*:*:*') in y['cpe23Uri'] and (not 'versionEndIncluding' in y and not 'versionEndExcluding' in y)]) >0)):
                       if len([ y for x in config['children'] for y in x['cpe_match'] if y['cpe23Uri'] == str(asset_cve['cpeID'])]) > 0:
                           assets_cve.append(asset_cve)
#                          print("WE GOT AND")
                elif config['operator'] == 'OR':
                    if (len([x for x in config['cpe_match'] if str(asset_cve['osType']) in x['cpe23Uri'] and str(asset_cve['osVersion']) in x['cpe23Uri']]) > 0):
#                       print("WE GOT OR")
                        assets_cve.append(asset_cve)
        return assets_cve
