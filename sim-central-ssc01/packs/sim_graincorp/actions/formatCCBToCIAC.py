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
      csv_file_path = "/opt/stackstorm/packs/sim_graincorp/inputs/billingDetails.csv"

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
                "Charge_Amt": row[14], #Charge_Amt
                "Service_Id": row[12],  #Service_Id"
                "Charged_Amt": row[14],  
                "ServiceProfile": "",
                "waive_charge": "",
                "waive_days": "",
                "waive_ticket_num": "",
                "waive_requestBy": "",
                "IDCol": row[15], #Row_id
            }
            
            billing_data.append(billing_object)
        txt_file_path = '/opt/stackstorm/packs/sim_graincorp/inputs/unique_vms.txt'
        

        try:
        # Open the text file in read mode
            with open(txt_file_path, 'r') as txt_file:
                json_data = json.load(txt_file)
        except Exception as e:
            print(e)

        unique_vms_list= json_data['vms']['vmName']
        unique_vm_configs=[]

        for vms in unique_vms_list:
            #if vms != "sydnwsql01":
                #continue
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
            cpuHoursvolume=0
            cpuHoursduration=0
            memHoursVolume=0
            memHoursDuration=0
            chargeAmtForBackupEnabled=0
            SIFriendlyName=""
            ethvmid=""
            storHours = 0
            LicVolume = 0
            LicCost = 0

            testcharge=0

            for obj in billing_data:
               if vms == obj["vmName"]:
                    #monthly_charge_amt = float(float(obj["Charge_Amt"]) * int(obj["Duration"]))
                    SIFriendlyName=obj["vmName"]
                    ethvmid=obj["ethvmid"]
                    if obj["Resource"]=="BackupLic" and obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":
                        #print("Backuplic",obj['Charge_Amt'], obj['Volume'])
                        testcharge+=float(obj['Charge_Amt'])
                        backupBase+=float(obj["Charge_Amt"])
                    if obj["Resource"] == "LIC" and obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":
                        #print("lic",obj['Charge_Amt'], obj['Volume'])
                        testcharge+=float(obj['Charge_Amt'])
                        LicVolume += float(obj["Volume"])
                        LicCost += float(obj['Charge_Amt'])
                        cpuTotal += float(obj['Charge_Amt'])
                    if obj["Resource"]=="Backup" and obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":
                        #print("Backup vol!=1",obj['Charge_Amt'], obj['Volume'])
                        testcharge+=float(obj['Charge_Amt'])
                        backupProt+=float(obj["Charge_Amt"])
                        chargeAmtForBackupEnabled=float(obj["Charge_Amt"])
                    if obj["Resource"]=="DrLic" and obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":
                        testcharge+=float(obj['Charge_Amt'])
                        #print("DrLic",obj['Charge_Amt'], obj['Volume'])
                        drLicensing+=float(obj["Charge_Amt"])  
                    if obj["Resource"]=="DrDisk" and obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":   
                        testcharge+=float(obj['Charge_Amt'])
                        #print("DrDisk",obj['Charge_Amt'], obj['Volume'])
                        drDisk+=float(obj["Charge_Amt"])   
                    if obj["Resource"]=="DrCPU" and obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":
                        testcharge+=float(obj['Charge_Amt'])
                        #print("DrCpu",obj['Charge_Amt'], obj['Volume'])
                        drCPU+=float(obj["Charge_Amt"])  
                    if obj["Resource"]=="DrRAM" and obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":
                        testcharge+=float(obj['Charge_Amt'])
                        #print("DrRam",obj['Charge_Amt'], obj['Volume'])
                        drRam+=float(obj["Charge_Amt"])
                    if obj["Resource"]=="CPU":
                        if obj["Volume"]!="" and obj["Volume"]!="N/A":
                            cpuHoursvolume=float(obj["Volume"])
                        if obj["Duration"]!="" and obj["Duration"]!="N/A":    
                            cpuHoursduration=float(obj["Duration"])
                        if obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":    
                            cpuTotal+=float(obj["Charge_Amt"])
                        testcharge+=float(obj['Charge_Amt'])
                    if obj["Resource"]=="RAM":
                        if obj["Volume"]!="" and obj["Volume"]!="N/A":
                            memHoursVolume=float(obj["Volume"])
                        if obj["Duration"]!="" and obj["Duration"]!="N/A":    
                            memHoursDuration=float(obj["Duration"])
                        if obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":    
                            memTotal+=float(obj["Charge_Amt"])
                        testcharge+=float(obj['Charge_Amt'])
                    if obj["Resource"]=="DISK":
                        storHours += round(float(obj["Duration"])*float(obj["Volume"]))
                        if obj["Charge_Amt"]!="" and obj["Charge_Amt"]!="N/A":
                            storTotal+=float(obj["Charge_Amt"]) 
                        testcharge+=float(obj['Charge_Amt'])


            #print("Testcharge",testcharge)

            backupTotal=round(float(backupBase)+float(backupProt),6)
            drTotal=round(float(drCPU)+float(drRam)+float(drDisk)+float(drLicensing),6)
            subTotal=round(float(cpuTotal)+float(memTotal)+float(storTotal),6)
            vmTotal = round(float(subTotal)+float(backupTotal)+float(drTotal),6)
            CurrentRate = round(float(vmTotal),6)
            vCPUHours=round(float(cpuHoursvolume)*float(cpuHoursduration),6)
            MemHours=round(float(memHoursVolume)*float(memHoursDuration),6)
            ChargevCPU=round(float(cpuTotal),6)
            ChargeMem=round(float(memTotal),6)
            ChargeStorage=round(float(storTotal),6)
            Subtotal=subTotal
            BackupBase=float(backupBase)
            BackupProtected=round(float(backupProt),2)
            BackupAgentProtected=0
            ethDR=round(float(drTotal),6)
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
            vm_object["StorHours"]=storHours
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
            vm_object["LicCost"] = LicCost
            vm_object["LicVolume"] = LicVolume

            unique_vm_configs.append(vm_object)


        txt_file_output = "/opt/stackstorm/packs/sim_graincorp/inputs/formatccbtociacoutput.txt"
        
        try:
            with open(txt_file_output, 'w') as txt_file:
                json.dump(unique_vm_configs, txt_file)    
        except Exception as e:
            print(e)
            
        return {
            'data': unique_vm_configs
        }
