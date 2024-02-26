from st2common.runners.base_action import Action
import csv
import json

class UniqueVMs(Action):
    def __init__(self, config=None, action_service=None):
        super(UniqueVMs, self).__init__(config, action_service)

    def run(self):
      billing_details=[]

      csv_file_path = "/opt/stackstorm/packs/sim_graincorp/inputs/billingDetails.csv"
      
      try:
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)

            # Specify the starting row number (0-based index)
            starting_row = 8

            # Process rows starting from the specified row
            for line_number, row in enumerate(csv_reader):
                if line_number > starting_row:
                    if(len(row)<=3):
                        break

                    billing_object = {
                        "Account Code": row[1], #Account_Nbr
                "ethvmid": row[2], #EthVmId
                "vmName": row[3], #VmName
                "Product_Code": row[11], #Prod_Code
                "Billing_Type": "",
                "Resource": row[4], #usg
                "Storage_Tier": row[5], #tier
                "Device_Id": "",
                "deviceKey": "",
                "Volume": row[6],  #vol
                "Duration": row[9],  #usg_hours
                "Rate_Flag": "",
                "Rate": "",
                "Charge_Amt": row[13], #Charge_Amt
                "Service_Id": row[12],  #Service_Id"
                "Charged_Amt": row[13],  
                "ServiceProfile": "",
                "waive_charge": "",
                "waive_days": "",
                "waive_ticket_num": "",
                "waive_requestBy": "",
                "IDCol": row[15], #Row_id
                    }
            
                    billing_details.append(billing_object)
                    
      except Exception as e:
        print(e)

      unique_vm_names = set(item["vmName"] for item in billing_details)
      vmName_object = {
            "vms": {
                "vmName": [
                ]
              }
      }

      vmName_object["vms"]["vmName"] = list(unique_vm_names)

      txt_file_output = "/opt/stackstorm/packs/sim_graincorp/inputs/unique_vms.txt"
      try:
         with open(txt_file_output, 'w') as txt_file:
            json.dump(vmName_object, txt_file) 
      except Exception as e:
          print(e)

      return {
         'msg':vmName_object
      }
