from st2common.runners.base_action import Action
import requests

class GetNetDbDetails(Action):
    def run(self):
        try:
            url = "https://netdb.essist.com.au/api/v1/customersite/?customer=36"
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
                    "CustomerID": str(entry.get("customer", "")),
                    "SiteID": str(entry.get("customersitestatus",{}).get("customersite","")) if entry.get("customersitestatus") else "",
                    "SiteName": str(entry.get("name", "")),
                    "SiteAddress": str(entry.get("location",{}).get("print_address", "")) if entry.get("location") else "",
                    "LocID": "",
                    "Managed": str(entry.get("managed", ""))
                }
                formatted_data.append(formatted_entry)
                primary_id += 1

            return formatted_data
        except requests.exceptions.RequestException as e:
            return (False, "Error making the HTTP request: {}".format(str(e)))
        except Exception as e:
            return (False, "An unexpected error occurred: {}".format(str(e)))
