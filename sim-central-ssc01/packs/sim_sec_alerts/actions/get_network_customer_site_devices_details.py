from st2common.runners.base_action import Action
import requests

class GetNetDbDetails(Action):
    def run(self):
        try:
            url = "https://netdb.essist.com.au/api/v1/cpe/assurancedashboard/?customer=36"
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

            for entry in data:
                formatted_entry = {
                    "PrimaryID": str(primary_id),
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
                primary_id += 1

            return formatted_data
        except requests.exceptions.RequestException as e:
            return (False, "Error making the HTTP request: {}".format(str(e)))
        except Exception as e:
            return (False, "An unexpected error occurred: {}".format(str(e)))
