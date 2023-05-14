import os
import csv
from datetime import datetime
from datetime import date
import json
import requests
import sys
import meraki
import argparse
from dotenv import load_dotenv
load_dotenv()


ap = argparse.ArgumentParser()

ap.add_argument("--action", required=True, help="Do you wish to isolate the site(allow) or reestablish the vpn connection(deny) ")
ap.add_argument("--sitename", required=False, help="Exact name of site that you wish to perform the action on as given in Meraki Dashboard")
args = vars(ap.parse_args())

action=  args['action']
sitename= args['sitename']



def change_dest():
    d = next(item for item in existing_rules if item['comment'] == 'Test-CR#CHG0031945-Dest')
    d['policy'] = policy
    d['destCidr'] = final_subnet
    

def change_src():
    d = next(item for item in existing_rules if item['comment'] == 'Test-CR#CHG0031945-Src')
    d['policy'] = policy
    d['srcCidr'] = final_subnet


if __name__ == '__main__':
    API_KEY = os.environ.get("api_key_china")
    dashboard = meraki.DashboardAPI(API_KEY,base_url='https://api.meraki.cn/api/v1/', print_console=False,output_log=False)
    site_subnet=[]
    tianjin_serial = "Q2EX-UNZ5-U26X"
    tianjin_port_id="23"

    guangzhou_serial = "Q2GX-E2H6-3W4P"
    guangzhou_port_id = "47"

    test_org_id = '850617379619605339'
    org_name="Pact Group China"
    try:
        vpn_firewall= dashboard.appliance.getOrganizationApplianceVpnVpnFirewallRules(test_org_id)
        existing_rules = vpn_firewall['rules']
    except meraki.exceptions.APIError as e:
        print(e)
        pass

    print ("List before deletion of dictionary : " +  json.dumps(existing_rules,indent=4))
    for i in range(len(existing_rules)):
        if (existing_rules[i]['comment'] == "Default rule"):
            del existing_rules[i]
            break


    org_id = "850617379619605339" #Pact China
    
    try:
        networks = dashboard.organizations.getOrganizationNetworks(org_id)
        for net in networks:
            if net['name'] == sitename:
                network_id = net['id']
    except meraki.exceptions.APIError as e:
        print(e)
        pass

    try:
        network_subnets = dashboard.appliance.getNetworkApplianceVlans(network_id)
        for subnet in network_subnets:
            subnets =subnet['subnet']
            site_subnet.append(subnets)
    except meraki.exceptions.APIError as e:
        print(e)
        pass

    if action == "restore":
        port_status = True
        policy ="allow"
        final_subnet="10.255.255.0/24"
    else:
        policy = "deny"
        port_status = False
        final_subnet = ",".join(site_subnet)

    #Disable switch ports to isolate hub site
    if sitename == "CN - 120 - CSI Guangzhou":
        print(f'Updating Switch Port Status to -{port_status} for {sitename}')
        switchport_guangzhou = dashboard.switch.updateDeviceSwitchPort(guangzhou_serial,guangzhou_port_id,enabled=port_status)
    elif sitename == "CN - 122 - CSI Tianjin":
        print(f'Updating Switch Port Status to -{port_status} for {sitename}')
        switchport_tianjin = dashboard.switch.updateDeviceSwitchPort(tianjin_serial,tianjin_port_id,enabled=port_status)
    else:
        print(f'No known hub site, moving to updating rules')

    change_dest()
    change_src()

    print ("Final Update of dictionary : " +  json.dumps(existing_rules,indent=4))


    try:
        update_vpn_firewall= dashboard.appliance.updateOrganizationApplianceVpnVpnFirewallRules(test_org_id,rules=existing_rules)
    except meraki.exceptions.APIError as e:
        print(e)
        pass
