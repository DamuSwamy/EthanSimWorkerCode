from st2common.runners.base_action import Action
import requests

class GetNetDbDetails(Action):
    def run(self):
        try:
            url = "https://netdb.essist.com.au/api/v1/cpe/assurancedashboard/?customer=36"
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

            for entry in data:
                formatted_entry = {
                    "CustomerID": str(entry.get("customer_id", "")),
                    "SiteID": str(entry.get("site_id", "")),
                    "DeviceID": str(entry.get("id", "")),
                    "Managed": str(entry.get("managed", "")),
                    "Monitored": str(entry.get("monitored", "")),
                    "CPEType": str(entry.get("cpetype", "")),
                    "Manufacturer": str(entry.get("manufacturer", "")),
                    "DeviceName": str(entry.get("devicename", "")),
                    "IPAddress": str(entry.get("mgmt_ipv4", "")),
                    "Monitor_SW_NodeID": str(entry.get("monitor_sw_nodeid", "")),
                    "SNSRCount": str(entry.get("servicenowcase_counts", {}).get("service_request", "")),
                    "SNEventCount": str(entry.get("servicenowcase_counts", {}).get("event", "")),
                    "SNIncidentCount": str(entry.get("servicenowcase_counts", {}).get("incident", ""))
                }
                formatted_data.append(formatted_entry)

            return formatted_data
        except requests.exceptions.RequestException as e:
            return (False, "Error making the HTTP request: {}".format(str(e)))
        except Exception as e:
            return (False, "An unexpected error occurred: {}".format(str(e)))

