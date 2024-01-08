from st2common.runners.base_action import Action
from collections import defaultdict
from datetime import datetime, timedelta
import csv
import json

class FormatCCBToCIAC(Action):
    def __init__(self, config=None, action_service=None):
        super(FormatCCBToCIAC, self).__init__(config, action_service)

    def run(self):
        
      billing_data=[]

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
            
            billing_data.append(billing_object)


        txt_file_path = '/opt/stackstorm/packs/graincorp/unique_vms.txt'

        # Open the text file in read mode
        with open(txt_file_path, 'r') as txt_file:
          json_data = json.load(txt_file)

        unique_vms_list= json_data['vms']['vmName']
        unique_vm_configs=[]

        for vms in unique_vms_list:
            vm_object={}
            backupBase=0
            backupProt=0
            drCPU=0
            drRam=0
            drDisk=0
            drLicensing=0
            subTotal=0
            backupTotal=0 
            cpuTotal=0
            memTotal=0
            storTotal=0
            cpuHoursvolume=1
            cpuHoursduration=1
            memHoursVolume=1
            memHoursDuration=1
            chargeAmtForBackupEnabled=0
            SIFriendlyName=""
            ethvmid=""
            
            for obj in billing_data:
                if vms == obj["vmName"].lower():
                    SIFriendlyName=obj["vmName"]
                    ethvmid=obj["ethvmid"]
                    if obj["Resource"]=="BackupLicensing" and obj["Volume"]==1:
                        backupBase=obj["Charge_Amt"]
                    if obj["Resource"]=="Backup" and obj["Volume"]!=1:
                        backupProt+=float(obj["Charge_Amt"])
                    if obj["Resource"]=="Backup" and obj["Volume"]==1:
                        chargeAmtForBackupEnabled=obj["Charge_Amt"]
                    if obj["Resource"]=="drLicensing":
                        drLicensing=obj["Charge_Amt"]  
                    if obj["Resource"]=="drDisk":   
                        drDisk=obj["Charge_Amt"]   
                    if obj["Resource"]=="drCPUs":
                        drCPU=obj["Charge_Amt"]  
                    if obj["Resource"]=="drRAM":
                        drRam=obj["Charge_Amt"]
                    if obj["Resource"]=="numCPUs":
                        cpuHoursvolume=obj["Volume"]
                        cpuHoursduration=obj["Duration"]
                        cpuTotal+=float(obj["Charge_Amt"])
                    if obj["Resource"]=="memoryMB":
                        memHoursVolume=obj["Volume"]
                        memHoursDuration=obj["Duration"]
                        memTotal+=float(obj["Charge_Amt"])
                    if obj["Resource"]=="VirtualDisk":
                        storTotal+=float(obj["Charge_Amt"])

                    
            backupTotal=float(backupBase)+float(backupProt)
            drTotal=float(drCPU)+float(drRam)+float(drDisk)+float(drLicensing)
            subTotal=float(cpuTotal)+float(memTotal)+float(storTotal)
            vmTotal = float(subTotal)+float(backupTotal)+float(drTotal)
            CurrentRate = vmTotal
            vCPUHours=float(cpuHoursvolume)*float(cpuHoursduration)
            MemHours=float(memHoursVolume)*float(memHoursDuration)
            ChargevCPU=cpuTotal
            ChargeMem=memTotal
            ChargeStorage=storTotal
            Subtotal=subTotal
            BackupBase=backupBase
            BackupProtected=backupProt
            BackupAgentProtected=0
            ethDR=drTotal
            BackupEnabled="no"

            if chargeAmtForBackupEnabled>0:
                BackupEnabled="yes"
            else:
                BackupEnabled="no"  


            current_date = datetime.now()
            first_day_of_current_month = current_date.replace(day=1)
            last_day_of_prev_month = first_day_of_current_month - timedelta(days=1)
            formatted_prev_month = last_day_of_prev_month.strftime("%b-%Y")
            day_of_prev_month=15
            last_update_date = datetime(last_day_of_prev_month.year, last_day_of_prev_month.month, day_of_prev_month, 13, 34, 27)
            formatted_last_update = last_update_date.strftime("%Y-%m-%dT%H:%M:%S%z")    

            vm_object["Org"]="40000391"
            vm_object["Name"]=""
            vm_object["ServiceItemName"]=ethvmid
            vm_object["SIFriendlyName"]=SIFriendlyName
            vm_object["ServiceItemType"]="Virtual Server (VM)"
            vm_object["CurrentRate"]=CurrentRate
            vm_object["BillingPeriod"]=formatted_prev_month
            vm_object["LastUpdate"]=formatted_last_update
            vm_object["vCPUHours"]=vCPUHours
            vm_object["MemHours"]=MemHours
            vm_object["ChargevCPU"]=ChargevCPU
            vm_object["ChargeMem"]=ChargeMem
            vm_object["ChargeStorage"]=ChargeStorage
            vm_object["Subtotal"]=Subtotal
            vm_object["BackupBase"]=BackupBase
            vm_object["BackupProtected"]=BackupProtected
            vm_object["BackupAgentProtected"]=BackupAgentProtected
            vm_object["ethDR"]=ethDR
            vm_object["BackupEnabled"]=BackupEnabled
            vm_object["ProcessMethod"]="AUTOCCB"

            unique_vm_configs.append(vm_object)


        txt_file_output = "/opt/stackstorm/packs/graincorp/formatccbtociacoutput.txt"

        with open(txt_file_output, 'w') as txt_file:
          json.dump(unique_vm_configs, txt_file)    

        return {
            'data': unique_vm_configs
        }