import os
import csv
from datetime import datetime
from datetime import date
import json
import requests
import sys
import meraki
from dotenv import load_dotenv
load_dotenv()
import argparse


ap = argparse.ArgumentParser()

ap.add_argument("--password", required=True, help="Enter the new password you wish to set for the SSID ")
args = vars(ap.parse_args())

password=args['password']


def wifi_ssid():
    networks = dashboard.organizations.getOrganizationNetworks(org_id)
    for net in networks:
        print(f'{net["name"]}')
        if "configTemplateId" in net:
            print(f'Template Network')
            network_id = net['configTemplateId']
        else:            
            print(f'Non Template Network')
            network_id = net['id']
        ssids = dashboard.wireless.getNetworkWirelessSsids(network_id)
        for ssid in ssids:
            if ssid['name'] == "oOh!Test":
                print(f'{ssid["name"]} - {ssid["number"]} - {ssid["psk"]}\n')
                ssid_number = ssid["number"]
                try:
                    change_psk = dashboard.wireless.updateNetworkWirelessSsid(network_id, ssid_number, psk=password)
                    print(json.dumps(change_psk,indent=4))
                except Exception as e:
                    print(e)
                    return e
            else:
                continue

if __name__ == '__main__':
    api_key = os.environ.get("api_key")
    org_id=601793500207390695
    dashboard = meraki.DashboardAPI(api_key, print_console=False,output_log=False) 
    wifi_ssid()