from st2common.runners.base_action import Action
import requests
import json

class ReturnAssetVulDetails(Action):
    def run(self, asset, apiKey, **kwargs):
        assets_cve = []
        assets_os = []
        os_cves = []
        unique_pairs = set()
        #     assets = ast.literal_eval(asset)
        assets = asset
        #     asset_json = asset_record
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

        #             Start collection of asset vulnerabilities
                        
                cpe_id = asset_json['cpeID']
                api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe_id}"


                headers = {
                    "apiKey":apiKey}
                response = requests.get(api_url, headers=headers)
        #        print(response.text)
                response_json = response.json()
                for cve in response_json["vulnerabilities"]:
        #                   
                    asset_cve = {}
                    asset_cve['id']                    = cve['cve']['id']+ '|' +asset_json['cpeID']
                    asset_cve['AssetID']               = asset_json['AssetID']
                    asset_cve['cve']                   = cve['cve']['id']
                    asset_cve['cpeID']                 = asset_json['cpeID']
                    asset_cve['vendor']                = asset_json['MatchingVendor']
                    asset_cve['model']                 = asset_json['MatchingModel']
                    asset_cve['osType']                = asset_json['MatchingOSType']
                    asset_cve['osVersion']             = asset_json['MatchingOSVersion']
                    asset_cve['deviceName']            = asset_json['DeviceName']
                    asset_cve['netDBModel']            = asset_json['Model']
                    if "cvssMetricV31" in cve["cve"]["metrics"]:
                        asset_cve['impactBaseScore']       = cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
                        asset_cve['impactBaseSeverity']    = cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
                    elif "cvssMetricV3" in cve["cve"]["metrics"]:
                        asset_cve['impactBaseScore']       = cve["cve"]["metrics"]["cvssMetricV3"][0]["cvssData"]["baseScore"]
                        asset_cve['impactBaseSeverity']    = cve["cve"]["metrics"]["cvssMetricV3"][0]["cvssData"]["baseSeverity"]
                    elif "cvssMetricV2" in cve["cve"]["metrics"]:
                        asset_cve['impactBaseScore']       = "v2|" + str(cve["cve"]["metrics"]["cvssMetricV2"][0]["cvssData"]["baseScore"])
                        asset_cve['impactBaseSeverity']    = "v2|" + cve["cve"]["metrics"]["cvssMetricV2"][0]["baseSeverity"]
                    #else:
                        #asset_cve['impactBaseScore']       = "v2|" + str(cve['impact']['baseMetricV2']['cvssV2']['baseScore'])
                        #asset_cve['impactBaseSeverity']    = "v2|" + cve['impact']['baseMetricV2']['severity']
                    for config in cve['cve']['configurations'][0]['nodes']:
                        pair = (asset_cve['AssetID'], asset_cve['cve'])
                        if config['operator'] == 'AND':
        #                         print (len([x for x in config['children'][0]['cpeMatch'] if str(asset_cve['osType']) in x['criteria'] and str(asset_cve['osVersion']) in x['criteria']]))
                            if ((len([x for x in config['children'][0]['cpeMatch'] if str(asset_cve['osType']) in x['criteria'] and str(asset_cve['osVersion']) in x['criteria']]) > 0) or (len([y for y in config['children'][0]['cpeMatch'] if str(asset_cve['osType']+':*:*:*:*:*:*:*:*') in y['criteria'] and (not 'versionEndIncluding' in y and not 'versionEndExcluding' in y)]) >0)):
                                if len([ y for x in config['children'] for y in x['cpeMatch'] if y['criteria'] == str(asset_cve['cpeID'])]) > 0:
                                    if pair not in unique_pairs:
                                        assets_cve.append(asset_cve)
                                        unique_pairs.add(pair)
        #                                     print("WE GOT AND")
                        elif config['operator'] == 'OR':
                            if (len([x for x in config['cpeMatch'] if str(asset_cve['osType']) in x['criteria'] and str(asset_cve['osVersion']) in x['criteria']]) > 0):
                                if pair not in unique_pairs:
        #                                 print("WE GOT OR")
                                    assets_cve.append(asset_cve)
                                    unique_pairs.add(pair)

        print("Asset vulnerabilities scanned: "+ str(len(assets_cve)))
        # Collect OS vulnerabilities from NIST
        print("Starting OS vulnverabilites scan")
        for os in assets_os:
            cpe_id = os['oscpe']
            api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe_id}"

            apiKey = "afce07e1-68c2-4c6d-9ed8-75b075d508e8"

            headers = {
                "apiKey":apiKey}
            response = requests.get(api_url, headers=headers)
            response_json = response.json()
                    
        #         print("Response: "+ str(response_json))
            if response.status_code == 200:
                for resp_cve in response_json["vulnerabilities"]:
                    os_cve = {}
                    os_cve['cve']                                   = resp_cve['cve']['id']
                    os_cve['cpeID']                                 = os['oscpe']
                    if "cvssMetricV31" in resp_cve["cve"]["metrics"]:
                        os_cve['impactBaseScore']       = resp_cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
                        os_cve['impactBaseSeverity']    = resp_cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
                    elif "cvssMetricV3" in resp_cve["cve"]["metrics"]:
                        os_cve['impactBaseScore']       = resp_cve["cve"]["metrics"]["cvssMetricV3"][0]["cvssData"]["baseScore"]
                        os_cve['impactBaseSeverity']    = resp_cve["cve"]["metrics"]["cvssMetricV3"][0]["cvssData"]["baseSeverity"]
                    elif "cvssMetricV2" in resp_cve["cve"]["metrics"]:
                        os_cve['impactBaseScore']       = "v2|" + str(resp_cve["cve"]["metrics"]["cvssMetricV2"][0]["cvssData"]["baseScore"])
                        os_cve['impactBaseSeverity']    = "v2|" + resp_cve["cve"]["metrics"]["cvssMetricV2"][0]["baseSeverity"]
                    
                    for config in resp_cve['cve']['configurations'][0]['nodes']:
                        if config['operator'] == 'OR':
                            if ((len([x for x in config['cpeMatch'] if str(os['oscpe']) in x['criteria']]) > 0) or (len([y for y in config['cpeMatch'] if str(os['MatchingOSType']+':*:*:*:*:*:*:*:*') in y['criteria'] and (not 'versionEndIncluding' in y and not 'versionEndExcluding' in y)]) >0)):
                                os_cves.append(os_cve)
        #             print("os_cves: "+ str(os_cves))

        print("Add OS cves to collection")
        # Link the assets back up with the OS scan records
        for asset_json in assets:
            keys_to_check = ['MatchingVendor','MatchingOSType','MatchingOSVersion']
            if all(key in asset_json and asset_json[key] is not None for key, value in asset_json.items() if key in keys_to_check):
                check_match = "cpe:2.3:o:" + asset_json['MatchingVendor'] + ":" + asset_json['MatchingOSType'] + ":" + asset_json['MatchingOSVersion'] + ":*:*:*:*:*:*:*"
        #             print("Check match: " + str(check_match))
                for x in os_cves:
        #                 print("cpeID: " + str(x['cpeID']))
                    if x['cpeID'] == check_match:
        #                      print("cpeID: " + str(x['cpeID']))
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
        #                     print(asset_cve)
                        pair = (asset_cve['AssetID'], asset_cve['cve'])
                        if pair not in unique_pairs:
                            assets_cve.append(asset_cve)
                            unique_pairs.add(pair)
                            print("OS Record Added")
        print("Asset vulnerabilities scanned: "+ str(len(assets_cve))) 

        return assets_cve




