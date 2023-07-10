from st2common.runners.base_action import Action
import datetime
import json
import requests
import ast

class ReturnAssetVulDetails(Action):
    def run(self, asset, **kwargs):
        assets_cve = []
        assets_os = []
        os_cves = []
        unique_pairs = set()
#       assets = ast.literal_eval(asset)
        assets = asset
#       asset_json = asset_record
        print("Starting collection of Asset NIST data")
        for asset_json in assets:
            if asset_json['cpeID'] is not None:

                #Collect OS information for later use before requesting asset vulnerabilities
                keys_to_check = ['MatchingVendor','MatchingOSType','MatchingOSVersion']
                if all(key in asset_json and asset_json[key] is not None and asset_json[key] != "" for key, value in asset_json.items() if key in keys_to_check):
                    asset_os = {}
                    asset_os['oscpe']                  = "cpe:2.3:o:" + asset_json['MatchingVendor'] + ":" + asset_json['MatchingOSType'] + ":" + asset_json['MatchingOSVersion'] + ":*:*:*:*:*:*:*"
                    asset_os['MatchingOSType']         = asset_json['MatchingOSType']
                    if asset_os not in assets_os:
                        assets_os.append(asset_os)
                        print("assets_os: " + str(assets_os))

#               Start collection of asset vulnerabilities
                self.base_uri = 'https://services.nvd.nist.gov/rest/json/cves/1.0'
                endpoint = '{}?cpeMatchString={}&addOns=dictionaryCpes&apiKey=bbae5b04-84e6-4774-8e64-20094a6e6e73'.format(self.base_uri,asset_json['cpeID'])
                headers = {
                        'Content-Type': 'application/json'
                }
                response = requests.request('get', endpoint, headers=headers, data={})
#               print("Endpoint: "+ endpoint + ", status_code: "+ str(response.status_code))
                response_json = response.json()
                for cve in response_json['result']['CVE_Items']:
#                   print("cve: "+ str(cve['cve']['CVE_data_meta']['ID']))
                    asset_cve = {}
                    asset_cve['id']                    = cve['cve']['CVE_data_meta']['ID']+ '|' +asset_json['cpeID']
                    asset_cve['AssetID']               = asset_json['AssetID']
                    asset_cve['cve']                   = cve['cve']['CVE_data_meta']['ID']
                    asset_cve['cpeID']                 = asset_json['cpeID']
                    asset_cve['vendor']                = asset_json['MatchingVendor']
                    asset_cve['model']                 = asset_json['MatchingModel']
                    asset_cve['osType']                = asset_json['MatchingOSType']
                    asset_cve['osVersion']             = asset_json['MatchingOSVersion']
                    asset_cve['deviceName']            = asset_json['DeviceName']
                    asset_cve['netDBModel']            = asset_json['Model']
                    if 'baseMetricV3' in cve['impact']:
                        asset_cve['impactBaseScore']       = cve['impact']['baseMetricV3']['cvssV3']['baseScore']
                        asset_cve['impactBaseSeverity']    = cve['impact']['baseMetricV3']['cvssV3']['baseSeverity']
                    else:
                        asset_cve['impactBaseScore']       = "v2|" + str(cve['impact']['baseMetricV2']['cvssV2']['baseScore'])
                        asset_cve['impactBaseSeverity']    = "v2|" + cve['impact']['baseMetricV2']['severity']
                    for config in cve['configurations']['nodes']:
                        pair = (asset_cve['AssetID'], asset_cve['cve'])
                        if config['operator'] == 'AND':
#                           print (len([x for x in config['children'][0]['cpe_match'] if str(asset_cve['osType']) in x['cpe23Uri'] and str(asset_cve['osVersion']) in x['cpe23Uri']]))
                            if ((len([x for x in config['children'][0]['cpe_match'] if str(asset_cve['osType']) in x['cpe23Uri'] and str(asset_cve['osVersion']) in x['cpe23Uri']]) > 0) or (len([y for y in config['children'][0]['cpe_match'] if str(asset_cve['osType']+':*:*:*:*:*:*:*:*') in y['cpe23Uri'] and (not 'versionEndIncluding' in y and not 'versionEndExcluding' in y)]) >0)):
                                if len([ y for x in config['children'] for y in x['cpe_match'] if y['cpe23Uri'] == str(asset_cve['cpeID'])]) > 0:
                                    if pair not in unique_pairs:
                                        assets_cve.append(asset_cve)
                                        unique_pairs.add(pair)
#                                       print("WE GOT AND")
                        elif config['operator'] == 'OR':
                            if (len([x for x in config['cpe_match'] if str(asset_cve['osType']) in x['cpe23Uri'] and str(asset_cve['osVersion']) in x['cpe23Uri']]) > 0):
                                if pair not in unique_pairs:
#                                   print("WE GOT OR")
                                    assets_cve.append(asset_cve)
                                    unique_pairs.add(pair)

        print("Asset vulnerabilities scanned: "+ str(len(assets_cve)))
        # Collect OS vulnerabilities from NIST
        print("Starting OS vulnverabilites scan")
        for os in assets_os:
#           print("os: "+ str(os))
            base_uri = 'https://services.nvd.nist.gov/rest/json/cves/1.0'
            endpoint = '{}?cpeMatchString={}&addOns=dictionaryCpes&resultsPerPage=1000&apiKey=bbae5b04-84e6-4774-8e64-20094a6e6e73'.format(base_uri,os['oscpe'])
            headers = {
                'Content-Type': 'application/json'
                }
            response = requests.request('get', endpoint, headers=headers, data={})
            #   print("Endpoint: "+ endpoint + ", status_code: "+ str(response.status_code))
            response_json = response.json()
#           print("Response: "+ str(response_json))
            if response.status_code == 200:
                for resp_cve in response_json['result']['CVE_Items']:
                    os_cve = {}
                    os_cve['cve']                                   = resp_cve['cve']['CVE_data_meta']['ID']
                    os_cve['cpeID']                                 = os['oscpe']
                    if 'baseMetricV3' in resp_cve['impact']:
                        os_cve['impactBaseScore']       = resp_cve['impact']['baseMetricV3']['cvssV3']['baseScore']
                        os_cve['impactBaseSeverity']    = resp_cve['impact']['baseMetricV3']['cvssV3']['baseSeverity']
                    else:
                        os_cve['impactBaseScore']       = "v2|" + str(resp_cve['impact']['baseMetricV2']['cvssV2']['baseScore'])
                        os_cve['impactBaseSeverity']    = "v2|" + resp_cve['impact']['baseMetricV2']['severity']
                    for config in resp_cve['configurations']['nodes']:
                        if config['operator'] == 'OR':
                            if ((len([x for x in config['cpe_match'] if str(os['oscpe']) in x['cpe23Uri']]) > 0) or (len([y for y in config['cpe_match'] if str(os['MatchingOSType']+':*:*:*:*:*:*:*:*') in y['cpe23Uri'] and (not 'versionEndIncluding' in y and not 'versionEndExcluding' in y)]) >0)):
                                os_cves.append(os_cve)
#               print("os_cves: "+ str(os_cves))

        print("Add OS cves to collection")
        # Link the assets back up with the OS scan records
        for asset_json in assets:
            keys_to_check = ['MatchingVendor','MatchingOSType','MatchingOSVersion']
            if all(key in asset_json and asset_json[key] is not None for key, value in asset_json.items() if key in keys_to_check):
                check_match = "cpe:2.3:o:" + asset_json['MatchingVendor'] + ":" + asset_json['MatchingOSType'] + ":" + asset_json['MatchingOSVersion'] + ":*:*:*:*:*:*:*"
#               print("Check match: " + str(check_match))
                for x in os_cves:
#                   print("cpeID: " + str(x['cpeID']))
                    if x['cpeID'] == check_match:
#                        print("cpeID: " + str(x['cpeID']))
                        asset_cve = {}
                        asset_cve['id']                    = x['cve'] + '|' + x['cpeID']
                        asset_cve['AssetID']               = asset_json['AssetID']
                        asset_cve['cve']                   = x['cve']
                        asset_cve['cpeID']                 = asset_json['cpeID']
                        asset_cve['vendor']                = asset_json['MatchingVendor']
                        asset_cve['model']                 = asset_json['MatchingModel']
                        asset_cve['osType']                = asset_json['MatchingOSType']
                        asset_cve['osVersion']             = asset_json['MatchingOSVersion']
                        asset_cve['deviceName']            = asset_json['DeviceName']
                        asset_cve['netDBModel']            = asset_json['Model']
                        asset_cve['impactBaseScore']       = x['impactBaseScore']
                        asset_cve['impactBaseSeverity']    = x['impactBaseSeverity']
#                       print(asset_cve)
                        pair = (asset_cve['AssetID'], asset_cve['cve'])
                        if pair not in unique_pairs:
                            assets_cve.append(asset_cve)
                            unique_pairs.add(pair)
                            print("OS Record Added")
        print("Asset vulnerabilities scanned: "+ str(len(assets_cve)))
        return assets_cve
