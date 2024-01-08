from st2common.runners.base_action import Action
import csv
import json

class FixVCD(Action):
    def __init__(self, config=None, action_service=None):
        super(FixVCD, self).__init__(config, action_service)

    def run(self):
        
        csv_file_path = "/opt/stackstorm/packs/graincorp/servicecatalog3.csv"

        vm_details=[]

        with open(csv_file_path, 'r') as file:
          csv_reader = csv.reader(file)

          # Specify the starting row number (0-based index)
          starting_row = 34

          # Process rows starting from the specified row
          for line_number, row in enumerate(csv_reader):
              if line_number > starting_row:
                  if(len(row)<=3):
                    break
                  vm_object = {
                "ethZenossID": row[0],
                "Billable": row[1],
                "ethBackupAgent": row[2],
                "ethStorageTier": row[3],
                "ConsoleURL": row[4],
                "Moref": row[5],
                "NAME": row[6],
                "FriendlyName": row[7],
                "GuestOperatingSystemFamiy": row[8],
                "VMType": row[9],
                "VDCSIName": row[10],
                "PowerState": row[11],
                "CustomerNetworkName": row[12],
                "CustomerNetworkSIName": row[13],
                "PlatformElementID": row[14],
                "VMFullPath": row[15],
                "PrimaryIPAddress": row[16],
                "ServiceItemTypeName": row[17],
                "RunTimeLeaseExpirationDate": row[18],
                "Tenant": row[19],
                "organizationalUnitName": row[20],
                "customerName": row[21],
                "SubmittedDate": row[22],
                "AssignedDate": row[23],
                "podType": row[24],
                "ServiceItemTypeID": row[25],
                "ServiceItemID": row[26],
                "ComputerName": row[27],
                "GuestOperatingSystem": row[28],
                "VMTemplateName": row[29],
                "ServerSize": row[30],
                "vCPUs": row[31],
                "vRAMGB": row[32],
                "TotalDiskSizeGB": row[33],
                "NumberCores": row[34],
                "NumberCPUs": row[35],
                "TotalMemory": row[36],
                "OSDiskSizeGB": row[37],
                "STATUS": row[38],
                "FSMStatus": row[39],
                "StorageExpirationDate": row[40],
                "ManagementIPAddress": row[41],
                "ManagementNetworkName": row[42],
                "NumHDs": row[43],
                "VMName": row[44],
                "ethEnvironmentType": row[45],
                "ethCostCentre": row[46],
                "ethInternalOrderNumber": row[47],
                "PlanOrScriptType": row[48],
                "AlarmCount": row[49]
                }
                  vm_details.append(vm_object)



        new_json_object = []
        for obj in vm_details:
            vmName=""
            modified_obj = obj.copy()
            for key, value in obj.items():
                if key == "VMFullPath":
                    vmpath = value.split("/")
                    vmName = vmpath[-1]
                if key == "VMName":
                    vmNameValue = value
                    if(vmName != "" and vmName!=vmNameValue):
                        modified_obj[key] = vmName
                        modified_obj["changed"] = ""
            new_json_object.append(modified_obj)

        txt_file_output = "/opt/stackstorm/packs/graincorp/fixvcdoutput.txt"

        with open(txt_file_output, 'w') as txt_file:
          # Write the JSON data to the file
          json.dump(new_json_object, txt_file)    

        return {
            'data':new_json_object
        }