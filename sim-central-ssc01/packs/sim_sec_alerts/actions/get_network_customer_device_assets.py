from st2common.runners.base_action import Action
import requests

class GetNetDbDetails(Action):
    def run(self):
        try:
            url = "https://netdb.essist.com.au/api/v1/asset/assurancedashboard/?customer=36"
            auth_token = "d53d2028a7c8f872c31243af766f8fe6fe615594"

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
                original_modified_on = entry.get("lastupdated", "")
                
                # Extract the date and time part without milliseconds and time zone
                date_time_parts = original_modified_on.split(".")[0].split("+")[0]
                
                # Replace 'T' with a space character
                date_time_parts = date_time_parts.replace('T', ' ')

                # Handle cases where values are None
                warranty_date = str(entry.get("warranty_end_date", "")) if entry.get("warranty_end_date") is not None else ""
                last_date_support = str(entry.get("eol_last_date_support", "")) if entry.get("eol_last_date_support") is not None else ""
                #smartnet_coverage_end_date = str(entry.get("support_coverage_end_date", "")) if entry.get("support_coverage_end_date") is not None else ""
                
                
                formatted_entry = {
                    "PrimaryID": str(primary_id),
                    "CustomerID": str(entry.get("customer_id", "")),
                    "DeviceID": str(entry.get("cpe_id", "")),
                    "AssetID": str(entry.get("id", "")),
                    "ProductID": str(entry.get("productcode", "")),
                    "ProductName": str(entry.get("productname", "")),
                    "Serial": str(entry.get("serial_number", "")),
                    "WarrantyDate": warranty_date,
                    "Model": str(entry.get("productname", "")),
                    "LastDateSupport": last_date_support,
                    "Message": "",
                    "ModifiedOn": date_time_parts,  # Use the formatted date and time
                    "Status": str(entry.get("active", "")),
                    "SmartNetCoverageEndDate": "",
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
