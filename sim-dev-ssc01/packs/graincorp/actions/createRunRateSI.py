from st2common.runners.base_action import Action
import json

class CreateRunRateSI(Action):
    def __init__(self, config=None, action_service=None):
        super(CreateRunRateSI, self).__init__(config, action_service)

    def run(self):
        short_names={
        "GrainCorp-Storage_and_Logistics":"S&L",
        "GrainCorp-Corporate":"CORP",
        "GrainCorp-Marketing":"MKT",
        "GrainCorp-Group Infrastructure":"GRPINFR",
        "GrainCorp-Oils":"Oils",
        "GrainCorp":"GCRP"
        }

        txt_file_path = "/opt/stackstorm/packs/graincorp/joinccbtociacoutput.txt"
        with open(txt_file_path, 'r') as txt_file:
          joinccbtociacout = json.load(txt_file)
        join_ccb_to_ciac_output=joinccbtociacout

        run_rate_si_obj=[]

        for obj in join_ccb_to_ciac_output:
            modified_obj={}
            modified_obj["VMName"]=obj["SIFriendlyName"]
            modified_obj["BusinessUnit"]=short_names[obj["Org"]]

            if "ethEnvironmentType" in obj:
                modified_obj["SubUnit"]=obj["ethEnvironmentType"]
            else:
                modified_obj["SubUnit"]=""
            if "ethCostCentre" in obj:    
                modified_obj["CostCentre"]=obj["ethCostCentre"]
            else:
                modified_obj["CostCentre"]=""
            if "ethInternalOrderNumber" in obj:
                modified_obj["Project"]=obj["ethInternalOrderNumber"]
            else:
                modified_obj["Project"]=""
            if "vCPUHours" in obj:
                modified_obj["vCPU"]=obj["vCPUHours"]
            else:
                modified_obj["vCPU"]=""
            if "vRAM" in obj:    
                modified_obj["VRAM"]=obj["vRAM"]
            else:
                modified_obj["VRAM"]=""
            if "vDisk" in  obj:    
                modified_obj["vDisk"]=""
            else:
                modified_obj["vDisk"]=""
            if "vCPUHours" in obj:
                modified_obj["VCPUHours"]=obj["vCPUHours"]
            else:
                modified_obj["VCPUHours"]=""
            if "MemHours" in obj:
                modified_obj["GBMemHours"]=obj["MemHours"]
            else:
                modified_obj["GBMemHours"]=""
            if "GBStorHours" in obj:  
                modified_obj["GBStorHours"]=""
            if "ethDR" in obj:
                modified_obj["DR"]=obj["ethDR"]
            else:
                modified_obj["DR"]=""
            if "ethStorageTier" in obj:
                modified_obj["StorageTier"]=obj["ethStorageTier"]
            else:
                modified_obj["StorageTier"]=""
            if "ChargevCPU" in obj:
                modified_obj["ChargevCPU"]=obj["ChargevCPU"]
            else:
                modified_obj["ChargevCPU"]=""
            if "ChargeMem" in obj:
                modified_obj["ChargevRAM"]=obj["ChargeMem"]
            else:
                modified_obj["ChargevRAM"]=""
            if "ChargeStorage" in obj:
                modified_obj["ChargevDisk"]=obj["ChargeStorage"]
            else:
                modified_obj["ChargevDisk"]=""
            if "Moref" in obj:       
                modified_obj["Moref"]=obj["Moref"]
            else:
                modified_obj["Moref"]=""
            if "Subtotal" in obj:    
                modified_obj["ResourceSubtotal"]=obj["Subtotal"]
            else:
                modified_obj["ResourceSubtotal"]=""
            if "BackupBase" in obj:    
                if float(obj["BackupBase"]>0):
                    modified_obj["Backup"]="yes"
                else:
                    modified_obj["Backup"]="no"
            else:
                modified_obj["Backup"]=""       
            if "BackupAgentProtected" and "BackupAgentProtected" in obj:
                modified_obj["BackupCost"]=obj["BackupProtected"]+obj["BackupAgentProtected"]
            else:
                modified_obj["BackupCost"]=""
            if "CurrentRate" in obj:
                modified_obj["Total"]=obj["CurrentRate"]
            else:
                modified_obj["Total"]="" 
            if "BillingPeriod" in obj:           
                modified_obj["BillingPeriod"]=obj["BillingPeriod"]
            else:
                modified_obj["BillingPeriod"]=""   

            run_rate_si_obj.append(modified_obj)


        return {
            'data':run_rate_si_obj
        }
    
