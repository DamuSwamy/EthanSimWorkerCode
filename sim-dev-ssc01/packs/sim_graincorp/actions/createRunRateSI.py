from st2common.runners.base_action import Action
import json
import csv

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

        try:

            txt_file_path = "/opt/stackstorm/packs/sim_graincorp/inputs/joinccbtociacoutput.txt"
            with open(txt_file_path, 'r') as txt_file:
                joinccbtociacout = json.load(txt_file)
            join_ccb_to_ciac_output=joinccbtociacout
        
        except FileNotFoundError:
            print("File not found")

        except Exception as e:
            print(e)
            
        run_rate_si_obj=[]

        billing_month=""
        billing_year = ""

        for obj in join_ccb_to_ciac_output:
            modified_obj={
                "VMName":"",
                "BusinessUnit":"",
                "SubUnit":"",
                "CostCentre":"",
                "Project":"",
                "Licence":"",
                "vCPU":"",
                "vRAM":"",
                "vDisk":"",
                "vCPUHours":"",
                "GBMemHours":"",
                "GBStorHours":"",
                "DR":"",
                "StorageTier":"",
                "ChargeLicence":"",
                "ChargevCPU":"",
                "ChargevRAM":"",
                "ChargevDisk":"",
                "Moref":"",
                "ResourceSubtotal":"",
                "Backup":"",
                "BackupCost":"",
                "Total":"",
                "BillingPeriod":""

            }
            modified_obj["VMName"]=obj["SIFriendlyName"]
            modified_obj["BusinessUnit"]=short_names[obj["Org"]]

            if "ethEnvironmentType" in obj and obj["ethEnvironmentType"]!="None":
                modified_obj["SubUnit"]=obj["ethEnvironmentType"]
            else:
                modified_obj["SubUnit"]=""
            if "ethCostCentre" in obj and obj['ethCostCentre']=="<blank>":
                modified_obj["CostCentre"]=obj["ethCostCentre"]
            elif "ethCostCentre" in obj and len(obj['ethCostCentre'])>0 and obj['ethCostCentre']!="None":    
                modified_obj["CostCentre"]=float(obj["ethCostCentre"])
            else:
                modified_obj["CostCentre"]=""
            if "ethInternalOrderNumber" in obj and obj["ethInternalOrderNumber"]!="None":
                modified_obj["Project"]=obj["ethInternalOrderNumber"].strip()
            else:
                modified_obj["Project"]=""
            if "vCPU" in obj and len(obj['vCPU'])>0:
                modified_obj["vCPU"]=float(obj["vCPU"])
            else:
                modified_obj["vCPU"]=""
            if "vRAM" in obj and len(obj['vRAM'])>0:    
                modified_obj["vRAM"]=float(obj["vRAM"])
            else:
                modified_obj["vRAM"]=""
            if "TotalStorageGB" in  obj and len(obj['TotalStorageGB'])>0:    
                modified_obj["vDisk"]=float(obj['TotalStorageGB'])
            else:
                modified_obj["vDisk"]=""
            if "vCPUHours" in obj:
                modified_obj["vCPUHours"]=obj["vCPUHours"]
            else:
                modified_obj["vCPUHours"]=""
            if "MemHours" in obj:
                modified_obj["GBMemHours"]=obj["MemHours"]
            else:
                modified_obj["GBMemHours"]=""
            if "StorHours" in obj:  
                modified_obj["GBStorHours"]=obj['StorHours']
            else:
                modified_obj["GBStorHours"]=""
            if "ethDR" in obj and obj["ethDR"]!=0:
                modified_obj["DR"]=obj["ethDR"]
            else:
                modified_obj["DR"]=""
            if "ethStorageTier" in obj and obj["ethStorageTier"]!="None":
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
            if "Moref" in obj and len(modified_obj['Moref'])<=0:       
                modified_obj["Moref"]=obj["Moref"]
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
                billing_month = obj["BillingPeriod"].split('-')[0] 
                billing_year = obj["BillingPeriod"].split('-')[1] 
            else:
                modified_obj["BillingPeriod"]=""   
            if "LicVolume" in obj:
                modified_obj["Licence"]=obj["LicVolume"]
            else:
                modified_obj["Licence"]=""
            if "LicCost" in obj:
                modified_obj["ChargeLicence"]=obj["LicCost"]
            else:
                modified_obj["ChargeLicence"]=""
            run_rate_si_obj.append(modified_obj)
        


        csv_file_path = f"/opt/stackstorm/packs/sim_graincorp/output/MY_RUN_RATES_EXPORT_{billing_month+billing_year} - Final.csv"
        
        try:
            with open(csv_file_path, 'w', newline='') as csvfile:
                fields = run_rate_si_obj[0].keys()
                csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
                csvwriter.writeheader()
                csvwriter.writerows(run_rate_si_obj)


        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print(e)
        return {
            'month': billing_month,
            'year':billing_year,
            'data':run_rate_si_obj
        }
    
