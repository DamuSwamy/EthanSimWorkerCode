from st2common.runners.base_action import Action
import requests

class GetNetDbDetails(Action):
    def run(self):
        try:
            url = "https://netdb.essist.com.au/api/v1/customersite/?customer=36"
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
                    "CustomerID": str(entry.get("customer", "")),
                    "SiteID": str(entry.get("customersitestatus",{}).get("customersite","")) if entry.get("customersitestatus") else "",
                    "SiteName": str(entry.get("name", "")),
                    "SiteAddress": str(entry.get("location",{}).get("print_address", "")) if entry.get("location") else "",
                    "Managed": str(entry.get("managed", ""))
                }
                formatted_data.append(formatted_entry)

            return formatted_data
        except requests.exceptions.RequestException as e:
            return (False, "Error making the HTTP request: {}".format(str(e)))
        except Exception as e:
            return (False, "An unexpected error occurred: {}".format(str(e)))

