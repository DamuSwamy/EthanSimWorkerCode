# SiM ITSM Pack

## Introduction 

sim_itsm pack supplies actions for services related to IT Service Management to be used with SiM platform.

## Installing the pack

````
st2 pack install https://ethangroup.visualstudio.com/SPBU%20Automation/_git/sim_itsm

````

## Actions and Workflows

The following actions and workflows make up the pack ("`sim-itsm`"):

````
+-------------------------------------------+----------+---------------------------+
| ref                                       | pack     | description               |
+-------------------------------------------+----------+---------------------------+
| sim_itsm.create_connectwise_ticket        | sim_itsm | Create Connectwise Ticket |
| sim_itsm.deactivate_user                  | sim_itsm | Deactivate_User           |
| sim_itsm.update_Connectwise_ticket        | sim_itsm | Update Connectwise Ticket |
+-------------------------------------------+----------+---------------------------+

````

### sim_itsm.create_connectwise_Ticket

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 618490c70ce61f8d93b5cdca                                     |
| uid           | action:sim_itsm:create_connectwise_Ticket                    |
| ref           | sim_itsm.create_connectwise_Ticket                           |
| pack          | sim_itsm                                                     |
| name          | create_connectwise_Ticket                                    |
| description   | Create Connectwise Ticket                                    |
| enabled       | True                                                         |
| entry_point   | workflows/create_connectwise_ticket.yaml                     |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "board_id": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "board_id",                           |
|               |         "default": "103",                                    |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "company_id": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "company_id",                         |
|               |         "default": "2",                                      |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "team_id": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "team_id",                            |
|               |         "default": "210",                                    |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "source_id": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "source_id",                          |
|               |         "default": "8",                                      |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "ticket_summary": {                                      |
|               |         "type": "string",                                    |
|               |         "description": "ticket summary",                     |
|               |         "default": "SiM Ticket Creation",                    |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "ticket_initialDescription": {                           |
|               |         "description": "ticket_initialDescription",          |
|               |         "type": "string",                                    |
|               |         "default": "Testing,\\\\                             |
|               | SiM Automation,\\\\                                          |
|               | Test Ticket Creation",                                       |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "ticket_contactName": {                                  |
|               |         "description": "ticket_contactName",                 |
|               |         "type": "string",                                    |
|               |         "default": "PaulHooper",                             |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "auth_token": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "auth_token",                         |
|               |         "default": "ZXNzaXN0ZGV2K1VmQWRMMjl4dWkzMEJySWQ6aHpt |
|               | VWcxNmJvMzNlTXhCbQ==",                                       |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "client_id": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "client_id",                          |
|               |         "default": "13e3617a-b4d4-4c28-993c-80cd8cd2b88b",   |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/create_connectwise_ticket.meta.yaml                  |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_itsm.create_connectwise_ticket

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 61849658de1acdd8780e980b                                     |
| uid           | action:sim_itsm:create_connectwise_ticket                    |
| ref           | sim_itsm.create_connectwise_ticket                           |
| pack          | sim_itsm                                                     |
| name          | create_connectwise_ticket                                    |
| description   | Create Connectwise Ticket                                    |
| enabled       | True                                                         |
| entry_point   | workflows/create_connectwise_ticket.yaml                     |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "board_id": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "board_id",                           |
|               |         "default": "103",                                    |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "company_id": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "company_id",                         |
|               |         "default": "2",                                      |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "team_id": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "team_id",                            |
|               |         "default": "210",                                    |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "source_id": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "source_id",                          |
|               |         "default": "8",                                      |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "ticket_summary": {                                      |
|               |         "type": "string",                                    |
|               |         "description": "ticket summary",                     |
|               |         "default": "SiM Ticket Creation",                    |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "ticket_initialDescription": {                           |
|               |         "description": "ticket_initialDescription",          |
|               |         "type": "string",                                    |
|               |         "default": "Testing,\\\\                             |
|               | SiM Automation,\\\\                                          |
|               | Test Ticket Creation",                                       |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "ticket_contactName": {                                  |
|               |         "description": "ticket_contactName",                 |
|               |         "type": "string",                                    |
|               |         "default": "PaulHooper",                             |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "auth_token": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "auth_token",                         |
|               |         "default": "ZXNzaXN0ZGV2K1VmQWRMMjl4dWkzMEJySWQ6aHpt |
|               | VWcxNmJvMzNlTXhCbQ==",                                       |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "client_id": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "client_id",                          |
|               |         "default": "13e3617a-b4d4-4c28-993c-80cd8cd2b88b",   |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/create_connectwise_ticket.meta.yaml                  |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_itsm.deactivate_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 618490c70ce61f8d93b5cdcb                                     |
| uid           | action:sim_itsm:deactivate_user                              |
| ref           | sim_itsm.deactivate_user                                     |
| pack          | sim_itsm                                                     |
| name          | deactivate_user                                              |
| description   | Deactivate User                                              |
| enabled       | True                                                         |
| entry_point   | workflows/deactivate_user.yaml                               |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "user_id": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "user_id",                            |
|               |         "default": "801",                                    |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "auth_token": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "auth_token",                         |
|               |         "default": "ZXNzaXN0ZGV2K1VmQWRMMjl4dWkzMEJySWQ6aHpt |
|               | VWcxNmJvMzNlTXhCbQ==",                                       |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "client_id": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "client_id",                          |
|               |         "default": "13e3617a-b4d4-4c28-993c-80cd8cd2b88b",   |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/deactivate_user.meta.yaml                            |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_itsm.update_connectwise_ticket

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 618490c70ce61f8d93b5cdcc                                     |
| uid           | action:sim_itsm:update_connectwise_ticket                    |
| ref           | sim_itsm.update_connectwise_ticket                           |
| pack          | sim_itsm                                                     |
| name          | update_connectwise_ticket                                    |
| description   | Update Connectwise Ticket                                    |
| enabled       | True                                                         |
| entry_point   | workflows/update_connectwise_ticket.yaml                     |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "auth_token": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "auth_token",                         |
|               |         "default": "ZXNzaXN0ZGV2K1VmQWRMMjl4dWkzMEJySWQ6aHpt |
|               | VWcxNmJvMzNlTXhCbQ==",                                       |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "ticket_id": {                                           |
|               |         "type": "string",                                    |
|               |         "default": "720146",                                 |
|               |         "required": true,                                    |
|               |         "description": "ticket_id"                           |
|               |     },                                                       |
|               |     "ticket_text": {                                         |
|               |         "description": "ticket_text",                        |
|               |         "type": "string",                                    |
|               |         "default": "Testing From SiM Automation Test Ticket  |
|               | Update",                                                     |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "detailDescriptionFlag": {                               |
|               |         "description": "detailDescriptionFlag",              |
|               |         "type": "string",                                    |
|               |         "default": "true",                                   |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "internalAnalysisFlag": {                                |
|               |         "description": "internalAnalysisFlag",               |
|               |         "type": "string",                                    |
|               |         "default": "false",                                  |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "resolutionFlag": {                                      |
|               |         "type": "string",                                    |
|               |         "description": "resolutionFlag",                     |
|               |         "default": "false",                                  |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "issueFlag": {                                           |
|               |         "description": "issueFlag",                          |
|               |         "type": "string",                                    |
|               |         "required": true,                                    |
|               |         "default": "false"                                   |
|               |     },                                                       |
|               |     "client_id": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "client_id",                          |
|               |         "default": "13e3617a-b4d4-4c28-993c-80cd8cd2b88b",   |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/update_connectwise_ticket.meta.yaml                  |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````


## Prerequisites
The actions use the Connectwise APIs. Hence, an appropriate auth_token is required for these actions to work.
