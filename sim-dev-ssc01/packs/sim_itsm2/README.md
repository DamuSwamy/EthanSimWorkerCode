# ServiceNow Integration Pack

This integration allows bi-directional communication between StackStorm and ServiceNow REST API

# Overview

This action provides the basic REST primitives necessary to allow communication between StackStorm and ServiceNow. Ideally, this integration will be consumed in a site-specific integration pack that defines actions to specific ServiceNow specific business logic.

ServiceNow provides two videos to demonstrate how to setup Inbound and Outbound Web Service integrations.

* Inbound Integration - https://www.youtube.com/watch?v=EhxgEECd7mQ
* Outbound Integration - https://www.youtube.com/watch?v=WeeDW_iRM8k

An example pack has been included in this pack to show the integration of ServiceNow with these two integration examples.

## Configuration

### Outgoing Integration

Copy the example configuration [servicenow.yaml.example](./servicenow.yaml.example) to
`/opt/stackstorm/configs/servicenow.yaml` and edit as required. It should contain:

* `instance_name` - Upstream Instance Name (e.x.: stackstorm)
* `username` - Username of service account
* `password` - Password of service account
* `custom_params` - Common supported parameters that will be passed to all calls. [Example](https://developer.servicenow.com/app.do#!/rest_api_doc?v=jakarta&id=c_TableAPI)

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

### Incoming Integration

In your ServiceNow Outbound integration, REST endpoints accept JSON payloads. In addition, you must specify the following headers in your payload request:

```
Accept: application/json
Content-Type: application/json
```


## Actions

* `servicenow.approve_change` Set a change request number to approved
* `servicenow.assign_incident_to` assign an incident to a username
* `servicenow.get` - Get an entry using a dictionary query from a ServiceNow Table
* `servicenow.get_non_structured` - Get an entry using a string query from a ServiceNow Table
* `servicenow.get_incidents_assigned_to` - Get incidents assigned to a particular user
* `servicenow.update` - Update an entry in a ServiceNow Table
* `servicenow.set_incident_owner` - Set the owner of an incident record
* `servicenow.insert` - Insert an entry to a ServiceNow Table
* `servicenow.delete` - Delete an entry from a ServiceNow Table
* `servicenow.create_record` - Create an entry to a ServiceNow Table
* `servicenow.get_attachments` - Gets the metadata of all attachments to a ServiceNow Table
* `servicenow.get_attachment` - Gets the metadata of an attachment on a ServiceNow Table
* `servicenow.upload_attachment` - Uploads an attachment to an entry on a ServiceNow Table

## Examples

* Create_Record 
```
{"description":"test update","short_description":"test subject_please ignore","state":2,"assigned_to":"svc_sim_automation","notes_to_comments":true,"assignment_group":"Service Desk","category":"Service Request","subcategory":"User Administration","account":"Ethan","contact":"Aman Mujawar","service_offering":"Mitel UCaaS"}

sn_customerservice_general_case
```
* Update_Record
```
number CS00582XX
payload - {"description":"SiM Automation found that this ITSM ticket is older than 10 minutes hence may result into duplicate order so it decided to escalate this ticket to engineer for further review, our engineer will review this request and verify if the order is already processed and do the needful\n\nOrder details follow\nCUSTOMER TENANT ID,PRODUCT NAME,OFFER ID,QUANTITY,BILLING FREQUENCY,TERM\nregex(\":\").replace(cbdf64d8-3641-436a-9665-ff6eb110d377,Visio Plan 2,b4d4b7f4-4089-43b6-9c44-de97b760fb11,1,monthly,P1Y:cbdf64d8-3641-436a-9665-ff6eb110d377,Office 365 E1,91fd106f-4b2c-4938-95ac-f54f74e9a239,2,monthly,P1Y:cbdf64d8-3641-436a-9665-ff6eb110d377,Enterprise Mobility Security E3,79c29af7-3cd0-4a6f-b182-a81e31dec84e,3,monthly,P1Y, \"\n\")","state":2,"assigned_to":null}
table - sn_customerservice_general_case
```
sn_customerservice_general_case

* Resolve_Record 
```
sn_customerservice_general_case

number - CS00592XX
payload - {"description":"SiM Automation has successfully completed the MSOL Order\nOrder ID - addf9260-0a99-4229-b4b0-a3680276a6eb\nBilling Cycle - monthly\nCurrency Code - AUD\n\nOrdered Product List -\n[['Visio Plan 2', 1, 'P1Y'], ['Office 365 E1', 140, 'P1Y'], ['Enterprise Mobility + Security E3', 5, 'P1Y']]","resolution_code":"Completed","close_notes":"Successful completion of MSOL order from SiM Automation ","state":3,"cause":"Ethan Online Request for MSOL License purchase from SiM Automation","assigned_to":"svc_sim_automation","closed_by":"84cf417087ff3410bd1d32e80cbb3502","closed_at":"2022-02-06 17:03:07","notes_to_comments":true}
table - sn_customerservice_general_case
```
