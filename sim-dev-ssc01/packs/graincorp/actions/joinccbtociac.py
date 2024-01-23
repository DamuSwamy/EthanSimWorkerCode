from st2common.runners.base_action import Action
import json
from datetime import datetime
import uuid

class JoinCCBToCIAC(Action):
    def __init__(self, config=None, action_service=None):
        super(JoinCCBToCIAC, self).__init__(config, action_service)

    def run(self):
      
      def generate_random_id():
        random_id = str(uuid.uuid4())
        # Format the UUID to match the specified pattern
        formatted_id = f"{random_id[:8]}-{random_id[9:13]}-{random_id[14:18]}-{random_id[19:23]}-{random_id[24:]}"

        return formatted_id
      
      
      txt_file_path = "/opt/stackstorm/packs/graincorp/fixvcdoutput.txt"

      current_datetime = datetime.now()

      # Open the text file in read mode
      with open(txt_file_path, 'r') as txt_file:
        fixvcdout = json.load(txt_file)

      vm_details_vcd_bracket_fixed=fixvcdout

      txt_file_path = '/opt/stackstorm/packs/graincorp/formatccbtociacoutput.txt'

      with open(txt_file_path, 'r') as txt_file:
          json_data = json.load(txt_file)


      format_ccb_to_ciac_output=json_data
      
      join_ccb_to_ciac=[]

      for obj in format_ccb_to_ciac_output:
            countActiveandRegistered=0
            countActiveandNotfound=0
            organizationalUnitNameForActiveAndRegistered=""
            nameForActiveAndRegistered=""
            serviceItemNameForActiveAndRegistered=""
            organizationalUnitNameForActiveAndNotFound=""
            nameForActiveAndNotFound=""
            serviceItemNameForActiveAndNotFound=""

            modified_obj = obj.copy()
            for vm_detail in vm_details_vcd_bracket_fixed:
                if obj["SIFriendlyName"]==vm_detail["VMName"]:
                    modified_obj["ethEnvironmentType"]=vm_detail["ethEnvironmentType"]
                    modified_obj["ethCostCentre"]=vm_detail["ethCostCentre"]
                    modified_obj["vCPU"]=vm_detail["vCPUs"]
                    modified_obj["vRAM"]=vm_detail["vRAMGB"]
                    modified_obj["ethStorageTier"]=vm_detail["ethStorageTier"]
                    modified_obj["Moref"]=vm_detail["Moref"]
                    modified_obj['TotalStorageGB']=vm_detail['TotalStorageGB']

                    modified_obj["ethInternalOrderNumber"]=vm_detail["ethInternalOrderNumber"]
                    if vm_detail["STATUS"].upper()=="ACTIVE" and vm_detail["FSMStatus"].upper()=="REGISTERED":
                        organizationalUnitNameForActiveAndRegistered=vm_detail["organizationalUnitName"]
                        nameForActiveAndRegistered=vm_detail["NAME"]+current_datetime.strftime("%Y%m")
                        serviceItemNameForActiveAndRegistered=vm_detail["NAME"]
                        countActiveandRegistered+=1

                    if vm_detail["STATUS"].upper()=="ACTIVE" and vm_detail["FSMStatus"].upper()=="NOTFOUND":
                        organizationalUnitNameForActiveAndNotFound=vm_detail["organizationalUnitName"]
                        nameForActiveAndNotFound=vm_detail["NAME"]+current_datetime.strftime("%Y%m")
                        serviceItemNameForActiveAndNotFound=vm_detail["NAME"]
                        countActiveandNotfound+=1


            if countActiveandRegistered == 1:
                modified_obj["Org"]=organizationalUnitNameForActiveAndRegistered
                modified_obj["Name"]=nameForActiveAndRegistered
                modified_obj["ServiceItemName"]=serviceItemNameForActiveAndRegistered
            elif countActiveandNotfound==1:
                modified_obj["Org"]=organizationalUnitNameForActiveAndNotFound
                modified_obj["Name"]=nameForActiveAndNotFound
                modified_obj["ServiceItemName"]=serviceItemNameForActiveAndNotFound

            else:
                modified_obj["Org"]="GrainCorp"
                modified_obj["Name"]= generate_random_id()

            join_ccb_to_ciac.append(modified_obj)

      txt_file_output = "/opt/stackstorm/packs/graincorp/joinccbtociacoutput.txt"

      with open(txt_file_output, 'w') as txt_file:
          json.dump(join_ccb_to_ciac, txt_file) 

      return {
            'data': join_ccb_to_ciac
      }
