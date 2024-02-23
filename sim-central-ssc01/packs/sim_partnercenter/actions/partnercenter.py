from st2common.runners.base_action import Action
import requests
from datetime import datetime, timedelta
import pytz

class PartnerCenter(Action):
    def __init__(self, config=None, action_service=None):
        super(PartnerCenter, self).__init__(config, action_service)

    def run(self, tenant_id, client_id, client_secret):
        def get_access_token(tenant_id, client_id, client_secret):
            url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
            body = {
                "client_id": client_id,
                "resource": "https://graph.windows.net",
                "client_secret": client_secret,
                "grant_type": "client_credentials"
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            response = requests.post(url, data=body, headers=headers)
            if response.status_code == 200:
                return response.json()["access_token"]
            else:
                print("Error:", response.status_code, response.text)
                return None


        def get_partner_customers(auth_token):
            url = "https://api.partnercenter.microsoft.com/v1/customers"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {auth_token}"
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return {
                    "customer_list": data["items"],
                    "total_customers": data["totalCount"]
                }
            else:
                print("Error:", response.status_code, response.text)
                return None


        access_token = get_access_token(tenant_id, client_id, client_secret)
        if access_token:
            customers = get_partner_customers(access_token)
            customer_list = customers["customer_list"]
            #print("Customer List:", customer_list)

            subscription_arr = []

            #print("Getting Subscriptions.....")
            for customer in customer_list:
                #print("Customer id :",customer['id'])
                customer_id = customer['id']
                url_base_subscriptions = f"https://api.partnercenter.microsoft.com/v1/customers/{customer_id}/subscriptions"
                
                headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
                }
                
                response_subscriptions = requests.get(url_base_subscriptions, headers=headers)
                subscriptions_data = response_subscriptions.json()

                for subscription in subscriptions_data['items']:
                    subscription_arr.append(subscription)

                if len(subscription_arr)>0: # re 
                    break
            
            print(subscription_arr)
            usage_arr = []
            for subscription in subscription_arr:
                subscription_id = subscription['id']

                self_uri = subscription['links']['self']['uri']

                self_uri_arr = self_uri.split('/')
                base_url = "https://api.partnercenter.microsoft.com"
                customer_tenant_id = self_uri_arr[2]
                subscription_id = self_uri_arr[4]
                australian_tz = pytz.timezone('Australia/Sydney')
                today = datetime.now(australian_tz)
                yesterday = today - timedelta(days=1)

                today_str = today.strftime("%Y-%m-%d")
                yesterday_str = yesterday.strftime("%Y-%m-%d")

                # start_time = "2024-02-20T00:00:00-08:00" 
                # end_time = "2024-02-21T00:00:00-08:00" 
                #start_time = f"{yesterday_str}T00:00:00-08:00"
                #end_time = f"{today_str}T00:00:00-08:00"
                
                start_time  = "2024-02-21T00:00:00-08:00"
                end_time  = "2024-02-22T00:00:00-08:00"

                granularity = "daily"
                show_details = True

                url = f"{base_url}/v1/customers/{customer_tenant_id}/subscriptions/{subscription_id}/utilizations/azure?start_time={start_time}&end_time={end_time}&granularity={granularity}&show_details={show_details}"

                headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "MS-RequestId": "e6a3b6b2-230a-4813-999d-57f883b60d38",
                "MS-CorrelationId": "a687bc47-8d08-4b78-aff6-5a59aa2055c2",
                "X-Locale": "en-US",
                }
            
                response_usage = requests.get(url, headers=headers)
                usage_data = response_usage.json()

                usage_arr.append(usage_data)

            # print(usage_arr)
            return {
                'usage_data':usage_arr
            }    

        else:
            return {
                'msg':'Failed to retrieve access token.'
            }
