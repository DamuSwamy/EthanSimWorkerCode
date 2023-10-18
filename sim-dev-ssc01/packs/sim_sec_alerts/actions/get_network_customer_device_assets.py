from st2common.runners.base_action import Action
import requests

class GetNetDbDetails(Action):
    def run(self):
        try:
            url = "https://netdb.essist.com.au/api/v1/asset/assurancedashboard/?customer=36"
            auth_token = "0ab414e6487e35477157f38640f58e8ae6a0df89"

            method = 'get'

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Token {}".format(auth_token)
            }

            response = requests.request(method, url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP error responses
            
            data = response.json()

            formatted_data = []
            primary_id = 1

            for entry in data:  # Loop through entries in the 'body' list
                formatted_entry = {
                    "PrimaryID": str(primary_id),
                    "CustomerID": str(entry.get("customer_id", "")),
                    "DeviceID": str(entry.get("cpe_id", "")),
                    "AssetID": str(entry.get("id", "")),
                    "ProductID": str(entry.get("productcode", "")),
                    "ProductName": str(entry.get("productname", "")),
                    "Serial": str(entry.get("serial_number", "")),
                    "WarrantyDate": str(entry.get("warranty_end_date", "")),
                    "Model": str(entry.get("productname", "")),
                    "LastDateSupport": str(entry.get("eol_last_date_support", "")),
                    "Message": "",
                    "ModifiedOn": str(entry.get("lastupdated", "")),
                    "Status": str(entry.get("active", "")),
                    "SmartNetCoverageEndDate": str(entry.get("support_coverage_end_date", "")),
                    "SmartNetContractType": str(entry.get("support_contract_type", "")),
                    "SNAssetSysID": str(entry["servicenow"].get("ethanprod_asset", ""))
                }
                formatted_data.append(formatted_entry)
                primary_id += 1

            return formatted_data
        except requests.exceptions.RequestException as e:
            return (False, "Error making the HTTP request: {}".format(str(e)))
        except Exception as e:
            return (False, "An unexpected error occurred: {}".format(str(e)))
