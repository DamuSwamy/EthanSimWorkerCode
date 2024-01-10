from st2common.runners.base_action import Action
import csv
import json

class UniqueVMs(Action):
    def __init__(self, config=None, action_service=None):
        super(UniqueVMs, self).__init__(config, action_service)

    def run(self):
      billing_details=[]

      csv_file_path = "/opt/stackstorm/packs/graincorp/billingDetails.csv"

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
                "Account Code": row[0],
                "ethvmid": row[1],
                "vmName": row[2],
                "Product_Code": row[3],
                "Billing_Type": row[4],
                "Resource": row[5],
                "Storage_Tier": row[6],
                "Device_Id": row[7],
                "deviceKey": row[8],
                "Volume": row[9],
                "Duration": row[10],
                "Rate_Flag": row[11],
                "Rate": row[12],
                "Charge_Amt": row[13],
                "Service_Id": row[14],
                "Charged_Amt": row[15],
                "ServiceProfile": row[16],
                "waive_charge": row[17],
                "waive_days": row[18],
                "waive_ticket_num": row[19],
                "waive_requestBy": row[20],
                "IDCol": row[21],
            }
            
            billing_details.append(billing_object)

      unique_vm_names = set(item["vmName"] for item in billing_details)
      vmName_object = {
            "vms": {
                "vmName": [
                ]
              }
      }

      vmName_object["vms"]["vmName"] = list(unique_vm_names)

      txt_file_output = "/opt/stackstorm/packs/graincorp/unique_vms.txt"

      with open(txt_file_output, 'w') as txt_file:
        json.dump(vmName_object, txt_file) 

      return {
         'msg':vmName_object
      }