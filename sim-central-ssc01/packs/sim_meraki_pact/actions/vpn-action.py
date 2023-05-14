import sqlite3
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

action=args['action']
sitename= args['sitename'] 




def change_dest():
    d = next(item for item in existing_rules if item['comment'] == 'Test-CR#CHG0030339-Dest')
    d['policy'] = policy
    d['destCidr'] = final_subnet
    

def change_src():
    d = next(item for item in existing_rules if item['comment'] == 'Test-CR#CHG0030339-Src')
    d['policy'] = policy
    d['srcCidr'] = final_subnet




def sync_sitesid():
    db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute('DELETE FROM pact_anz_vlans;')
    db_connection.commit()
    db_connection.close()
    try:
        pact_anz_networks = dashboard.organizations.getOrganizationNetworks(org_id)
        for net in pact_anz_networks:
            site_subnet=[]
            network_id = net['id']
            network_name= net['name']
            print(f'{network_name}\n')
            try:
                pact_anz_subnets = dashboard.appliance.getNetworkApplianceVlans(network_id)
                for subnet in pact_anz_subnets:
                    subnets = subnet['subnet']
                    site_subnet.append(subnets)    
            except meraki.exceptions.APIError as e:
                print(e)
                pass
            site_subnet_details = ", ".join(site_subnet)    
            db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db')
            db_cursor = db_connection.cursor()
            db_cursor.execute('INSERT INTO pact_anz_vlans(network_id, network_name,network_vlans) values (?,?,?)',(str(network_id),str(network_name),str(site_subnet_details)))
            db_connection.commit()
            db_connection.close()
    except meraki.exceptions.APIError as e:
        print(e)
        pass


def restore_multisite():
    print(f'Restoring one of the sites - {sitename}\n')
    db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db')
    db_cursor = db_connection.cursor()
    isolated_site_names = db_cursor.execute('SELECT network_name from pact_anz_isolatedsites WHERE network_name=?', (sitename,)).fetchall()
    if len(isolated_site_names) != 0:
        print(f'Site {isolated_site_names} isolated. Running process to restore site. \n')
        db_cursor.execute('DELETE from pact_anz_isolatedsites WHERE network_name=?', (sitename,))
        db_connection.commit()
        db_connection.close()
        print(f'Site {isolated_site_names} is now removed from isolated list. Processing final list of subnets')


        db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db')
        db_cursor = db_connection.cursor()
        isolated_network_lists = db_cursor.execute('SELECT network_id from pact_anz_isolatedsites').fetchall()
        db_connection.close()
        print(f'{len(isolated_network_lists)} sites are currently isolated')
        for isolated_sites in isolated_network_lists:
            isolated_sites_final=''.join(''.join(tup) for tup in isolated_sites)
            print(f'Currently Isolated sites - {isolated_sites_final}\n')
            try:
                net_subnets = dashboard.appliance.getNetworkApplianceVlans(isolated_sites_final)
                for subnet in net_subnets:
                    subnets =subnet['subnet']
                    site_network_vlans.append(subnets)
            except meraki.exceptions.APIError as e:
                print(e)
                pass
    else:
        print('Site is not currently isolated, no action to take \n')


def restore_singlesite():
    print(f'Running function to restore final site \n')
    db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute('DELETE FROM pact_anz_isolatedsites;')
    db_connection.commit()
    db_connection.close()
    print(f'All sites removed from Isolated Sites.')
    site_network_vlans.append("10.255.255.0/24")

def isolate_firstsite():
    print(f'No sites currently isolated\n')
    db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db')
    db_cursor = db_connection.cursor()
    site_network_id = db_cursor.execute('SELECT network_id from pact_anz_vlans WHERE network_name=?', (sitename,)).fetchall()
    site_network_id_final = ''.join(''.join(tup) for tup in site_network_id)
    try:
        net_subnets = dashboard.appliance.getNetworkApplianceVlans(site_network_id_final)
        for subnet in net_subnets:
            subnets =subnet['subnet']
            site_network_vlans.append(subnets)
    except meraki.exceptions.APIError as e:
        print(e)
        pass
    db_cursor.execute('INSERT INTO pact_anz_isolatedsites(network_id, network_name) values (?,?)',(str(site_network_id_final),str(sitename)))
    db_connection.commit()
    db_connection.close()


def isolate_site():
    db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db')
    db_cursor = db_connection.cursor()
    isolated_network_lists = db_cursor.execute('SELECT network_id from pact_anz_isolatedsites').fetchall()
    print(f'{len(isolated_count)} sites are currently isolated')
    for isolated_sites in isolated_network_lists:
        isolated_sites_final=''.join(''.join(tup) for tup in isolated_sites)
        print(f'Currently Isolated sites - {isolated_sites_final}\n')
        try:
            net_subnets = dashboard.appliance.getNetworkApplianceVlans(isolated_sites_final)
            for subnet in net_subnets:
                subnets =subnet['subnet']
                site_network_vlans.append(subnets)
        except meraki.exceptions.APIError as e:
            print(e)
            pass

    isolated_site_names = db_cursor.execute('SELECT network_name from pact_anz_isolatedsites WHERE network_name=?', (sitename,)).fetchall()
    if len(isolated_site_names) != 0:
        print(f'Site {isolated_site_names} already isolated. No action to take further \n')
    else:
        site_network_id = db_cursor.execute('SELECT network_id from pact_anz_vlans WHERE network_name=?', (sitename,)).fetchall()
        site_network_id_final = ''.join(''.join(tup) for tup in site_network_id)
        print(f'New site being isolated -{sitename} | {site_network_id_final}')
        
        try:
            new_net_subnets = dashboard.appliance.getNetworkApplianceVlans(site_network_id_final)
            for new_subnet in new_net_subnets:
                new_subnets = new_subnet['subnet']
                site_network_vlans.append(new_subnets)
        except meraki.exceptions.APIError as e:
            print(e)
            pass

        
        db_cursor.execute('INSERT INTO pact_anz_isolatedsites(network_id, network_name) values (?,?)',(str(site_network_id_final),str(sitename)))
        db_connection.commit()
        db_connection.close()
        

if __name__ == '__main__':
    site_network_vlans=[]

    #Database Connection and setup Section
    db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db') 
    db_cursor = db_connection.cursor()
    db_cursor.execute('''CREATE TABLE IF NOT EXISTS pact_anz_vlans ([network_id] VARCHAR, [network_name] VARCHAR,[network_vlans] VARCHAR(255))''')
    db_cursor.execute('''CREATE TABLE IF NOT EXISTS pact_anz_isolatedsites ([network_id] VARCHAR, [network_name] VARCHAR)''')   
    db_connection.commit()
    db_connection.close()

    #Meraki setup section
    API_KEY = os.environ.get("api_key")
    dashboard = meraki.DashboardAPI(API_KEY, print_console=False,output_log=False)
    
    #Sync PACT ANZ Sites and Subnets to DB
    org_id = '694834'
    org_name="PACT Group"

    sync_sitesid()
    

    test_org_id ='601793500207394197'
    test_org_name = 'Ethan Online - Test Organization'

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


    db_connection = sqlite3.connect('/home/ssadmin/sim_meraki_pact/actions/pact_sites_iso.db') 
    db_cursor = db_connection.cursor()
    isolated_count=db_cursor.execute('SELECT * from pact_anz_isolatedsites').fetchall()
    db_connection.close()
    print(f'Number of Sites currently isolated - {len(isolated_count)}\n')

    if len(isolated_count) == 0 and action != "restore":
        policy = "deny"
        isolate_firstsite()


    elif len(isolated_count) != 0 and action != "restore":
        policy = "deny"
        isolate_site()

    elif len(isolated_count) == 1 and action == "restore":
        print(f'Action is to Restore Final Isolated Site \n')
        policy ="allow"
        restore_singlesite()
    else:
        print(f'Running fucntion to restore when multiple sites are isolated')
        policy = "deny"
        restore_multisite()


    if action == "restore":
        #policy ="allow"
        final_subnet= ",".join(site_network_vlans)
    else:
        #policy = "deny"
        final_subnet = ",".join(site_network_vlans)

    

    change_dest()
    change_src()

    print ("Final Update of dictionary : " +  json.dumps(existing_rules,indent=4))

    try:
        update_vpn_firewall= dashboard.appliance.updateOrganizationApplianceVpnVpnFirewallRules(test_org_id,rules=existing_rules)
    except meraki.exceptions.APIError as e:
        print(e)
        pass