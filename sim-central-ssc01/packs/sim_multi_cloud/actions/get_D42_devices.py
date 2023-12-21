import json
import csv
import requests
import base64
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class get_D42_devices(Action):
    def run(self,bearer_token):
                url="https://cmdb.ecorp.systems/services/data/v1.0/query/"
                sql_query = """
SELECT device_pk,cid.instance_id as cid_instance_id , cf.identifier , virtualsubtype FROM view_device_v2 AS D LEFT OUTER JOIN view_hardware_v2 AS hw ON D.hardware_fk=hw.hardware_pk LEFT OUTER JOIN view_vendor_v1 AS v ON hw.vendor_fk=v.vendor_pk LEFT OUTER JOIN view_objectcategory_v1 AS OC ON D.objectcategory_fk = OC.objectcategory_pk LEFT OUTER JOIN view_customer_v1 AS cus ON D.customer_fk = cus.customer_pk LEFT OUTER JOIN view_device_custom_fields_flat_v2 AS cf ON D.device_pk = cf."device_fk" LEFT OUTER JOIN view_cloudinstance_v1 AS cid ON D.device_pk = cid."device_fk" where virtualsubtype = 'Azure Virtual Machine'
"""
                payload = {
                'query': sql_query
                }
                #bearer_token=bearer_token.decode('utf-8') 
                bearer_token = bearer_token.replace('\n', '').replace('\r', '')
                headers = {
                'Authorization': f'Bearer {bearer_token}',
                'Accept': 'application/json'  # Adjust content type based on your API requirements
                }
                data = requests.post(url, headers=headers, data=payload, verify=False)
                with open("/opt/stackstorm/packs/sim_multi_cloud/actions/dev42","wb") as filee:
                    filee.write(data.content)
                #print(data)
                print("Device details are successfully stored in dev42 file")
