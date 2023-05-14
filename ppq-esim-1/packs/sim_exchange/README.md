# SiM Exchange Pack

## Introduction 
sim_exchange pack supplies actions for services related to Microsoft Exchange to be used with the SiM platform.

## Installing the pack
````
st2 pack install https://ethangroup.visualstudio.com/SPBU%20Automation/_git/sim_exchange

````

## Actions and Workflows


The following actions and workflows make up the pack ("`sim-exchange`"):
````

+-------------------------------------+--------------+-----------------------------------------------+
| ref                                 | pack         | description                                   |
+-------------------------------------+--------------+-----------------------------------------------+
| sim_exchange.Delegate_Mailbox       | sim_exchange | Delegate_Mailbox                              |
| sim_exchange.Forward_Mailbox        | sim_exchange | Forward_Mailbox                               |
| sim_exchange.Get_Mailbox_Properties | sim_exchange | Get_Mailbox_Properties                        |
| sim_exchange.Share_Mailbox          | sim_exchange | Share_Mailbox                                 |
| sim_exchange.convert_mailbox        | sim_exchange | Convert mailbox                               |
+-------------------------------------+--------------+-----------------------------------------------+

````

### sim_exchange.AD_user_offboarding

````

+---------------+---------------------------------------------+
| Property      | Value                                       |
+---------------+---------------------------------------------+
| id            | 615a8e9c45844f57d0a5e063                    |
| uid           | action:sim_exchange:AD_user_offboarding     |
| ref           | sim_exchange.AD_user_offboarding            |
| pack          | sim_exchange                                |
| name          | AD_user_offboarding                         |
| description   | Sample AD offboarding orquesta automation   |
| enabled       | True                                        |
| entry_point   | workflows/AD_user_offboarding.yaml          |
| runner_type   | orquesta                                    |
| parameters    | {                                           |
|               |     "data": {                               |
|               |         "type": "object",                   |
|               |         "description": "input robot data.", |
|               |         "required": false                   |
|               |     }                                       |
|               | }                                           |
| metadata_file | actions/AD_user_offboarding.yaml            |
| notify        |                                             |
| output_schema |                                             |
| tags          |                                             |
+---------------+---------------------------------------------+

````

### sim_exchange.Delegate_Mailbox

````

+---------------+--------------------------------------------------+
| Property      | Value                                            |
+---------------+--------------------------------------------------+
| id            | 617012fec8101de118685b4f                         |
| uid           | action:sim_exchange:Delegate_Mailbox             |
| ref           | sim_exchange.Delegate_Mailbox                    |
| pack          | sim_exchange                                     |
| name          | Delegate_Mailbox                                 |
| description   | Delegate_Mailbox                                 |
| enabled       | True                                             |
| entry_point   | workflows/Delegate_Mailbox.yaml                  |
| runner_type   | orquesta                                         |
| parameters    | {                                                |
|               |     "user_email": {                              |
|               |         "type": "string",                        |
|               |         "description": "Email of the user",      |
|               |         "required": true                         |
|               |     },                                           |
|               |     "delegate_forward_email": {                  |
|               |         "type": "string",                        |
|               |         "description": "delegate_forward_email", |
|               |         "required": true                         |
|               |     }                                            |
|               | }                                                |
| metadata_file | actions/Delegate_Mailbox.meta.yaml               |
| notify        |                                                  |
| output_schema |                                                  |
| tags          |                                                  |
+---------------+--------------------------------------------------+

````

### sim_exchange.Forward_Mailbox

````

+---------------+----------------------------------------------------+
| Property      | Value                                              |
+---------------+----------------------------------------------------+
| id            | 61701889c8101de118685b5c                           |
| uid           | action:sim_exchange:Forward_Mailbox                |
| ref           | sim_exchange.Forward_Mailbox                       |
| pack          | sim_exchange                                       |
| name          | Forward_Mailbox                                    |
| description   | Forward_Mailbox                                    |
| enabled       | True                                               |
| entry_point   | workflows/Forward_Mailbox.yaml                     |
| runner_type   | orquesta                                           |
| parameters    | {                                                  |
|               |     "user_email": {                                |
|               |         "type": "string",                          |
|               |         "description": "Email of the user",        |
|               |         "required": true                           |
|               |     },                                             |
|               |     "forwarding_email_address": {                  |
|               |         "type": "string",                          |
|               |         "description": "forwarding_email_address", |
|               |         "required": true                           |
|               |     }                                              |
|               | }                                                  |
| metadata_file | actions/Forward_Mailbox.meta.yaml                  |
| notify        |                                                    |
| output_schema |                                                    |
| tags          |                                                    |
+---------------+----------------------------------------------------+

````

### sim_exchange.Get_Mailbox_Properties

````

+---------------+---------------------------------------------+
| Property      | Value                                       |
+---------------+---------------------------------------------+
| id            | 617019a6c8101de118685b63                    |
| uid           | action:sim_exchange:Get_Mailbox_Properties  |
| ref           | sim_exchange.Get_Mailbox_Properties         |
| pack          | sim_exchange                                |
| name          | Get_Mailbox_Properties                      |
| description   | Get_Mailbox_Properties                      |
| enabled       | True                                        |
| entry_point   | workflows/Get_Mailbox_Properties.yaml       |
| runner_type   | orquesta                                    |
| parameters    | {                                           |
|               |     "user_email": {                         |
|               |         "type": "string",                   |
|               |         "description": "Email of the user", |
|               |         "required": true                    |
|               |     }                                       |
|               | }                                           |
| metadata_file | actions/Get_Mailbox_Properties.meta.yaml    |
| notify        |                                             |
| output_schema |                                             |
| tags          |                                             |
+---------------+---------------------------------------------+

````

### sim_exchange.Get_Mailbox_Properties_improved

````

+---------------+-----------------------------------------------------+
| Property      | Value                                               |
+---------------+-----------------------------------------------------+
| id            | 617fd5e7253cc5f9cb6df17b                            |
| uid           | action:sim_exchange:Get_Mailbox_Properties_improved |
| ref           | sim_exchange.Get_Mailbox_Properties_improved        |
| pack          | sim_exchange                                        |
| name          | Get_Mailbox_Properties_improved                     |
| description   | Get_Mailbox_Properties_improved                     |
| enabled       | True                                                |
| entry_point   | workflows/Get_Mailbox_Properties_improved.yaml      |
| runner_type   | orquesta                                            |
| parameters    | {                                                   |
|               |     "user_email": {                                 |
|               |         "type": "string",                           |
|               |         "description": "Email of the user",         |
|               |         "required": true                            |
|               |     }                                               |
|               | }                                                   |
| metadata_file | actions/Get_Mailbox_Properties_improved.meta.yaml   |
| notify        |                                                     |
| output_schema |                                                     |
| tags          |                                                     |
+---------------+-----------------------------------------------------+

````

### sim_exchange.Share_Mailbox

````

+---------------+---------------------------------------------+
| Property      | Value                                       |
+---------------+---------------------------------------------+
| id            | 616fe9e1c8101de118685b05                    |
| uid           | action:sim_exchange:Share_Mailbox           |
| ref           | sim_exchange.Share_Mailbox                  |
| pack          | sim_exchange                                |
| name          | Share_Mailbox                               |
| description   | Share_Mailbox                               |
| enabled       | True                                        |
| entry_point   | workflows/Share_Mailbox.yaml                |
| runner_type   | orquesta                                    |
| parameters    | {                                           |
|               |     "user_email": {                         |
|               |         "type": "string",                   |
|               |         "description": "Email of the user", |
|               |         "required": true                    |
|               |     }                                       |
|               | }                                           |
| metadata_file | actions/Share_Mailbox.meta.yaml             |
| notify        |                                             |
| output_schema |                                             |
| tags          |                                             |
+---------------+---------------------------------------------+

````

### sim_exchange.convert_delegate_forward_mailbox

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 618112c8253cc5f9cb6df1b6                                     |
| uid           | action:sim_exchange:convert_delegate_forward_mailbox         |
| ref           | sim_exchange.convert_delegate_forward_mailbox                |
| pack          | sim_exchange                                                 |
| name          | convert_delegate_forward_mailbox                             |
| description   | convert_delegate_forward_mailbox                             |
| enabled       | True                                                         |
| entry_point   | workflows/convert_delegate_forward_mailbox.yaml              |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "certificate_file_path": {                               |
|               |         "type": "string",                                    |
|               |         "default": "certificate",                            |
|               |         "description": "Certificate file path",              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "default": "Administrator",                          |
|               |         "required": true,                                    |
|               |         "description": "username"                            |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "organisation": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "organisation",                       |
|               |         "default": "etest.systems",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "host": {                                                |
|               |         "type": "string",                                    |
|               |         "description": "host",                               |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com",                              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "user_email": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "User email to act as identify ",     |
|               |         "default": "sim.testuser01@etest.systems",           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "delegate_forward_email": {                              |
|               |         "type": "string",                                    |
|               |         "default": "Teams.Test1@etest.systems",              |
|               |         "description": "delegate_forward_email",             |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "forwarding_email_address": {                            |
|               |         "type": "string",                                    |
|               |         "default": "Teams.Test1@etest.systems",              |
|               |         "description": "forwarding_email_address",           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "type": {                                                |
|               |         "type": "string",                                    |
|               |         "description": "Type of mailbox to convert to e.g    |
|               | Shared",                                                     |
|               |         "default": "Shared",                                 |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "app_id": {                                              |
|               |         "type": "string",                                    |
|               |         "description": "App Id",                             |
|               |         "default": "f9954a04-347a-4a74-be7e-90deceb9ef7a",   |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/convert_delegate_forward_mailbox.meta.yaml           |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_exchange.convert_mailbox

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 6171a09ac8101de118685c83                                     |
| uid           | action:sim_exchange:convert_mailbox                          |
| ref           | sim_exchange.convert_mailbox                                 |
| pack          | sim_exchange                                                 |
| name          | convert_mailbox                                              |
| description   | Convert mailbox                                              |
| enabled       | True                                                         |
| entry_point   | workflows/convert_mailbox.yaml                               |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "certificate_file_path": {                               |
|               |         "type": "string",                                    |
|               |         "description": "Certificate file path",              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "default": "Administrator",                          |
|               |         "required": true,                                    |
|               |         "description": "username"                            |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "organisation": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "organisation",                       |
|               |         "default": "etest.systems",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "host": {                                                |
|               |         "type": "string",                                    |
|               |         "description": "host",                               |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com",                              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "user_email": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "User email to act as identify ",     |
|               |         "default": "sim.testuser01@etest.systems",           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "type": {                                                |
|               |         "type": "string",                                    |
|               |         "description": "Type of mailbox to convert to e.g    |
|               | Shared",                                                     |
|               |         "default": "Shared",                                 |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "app_id": {                                              |
|               |         "type": "string",                                    |
|               |         "description": "App Id",                             |
|               |         "default": "f9954a04-347a-4a74-be7e-90deceb9ef7a",   |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/convert_mailbox.meta.yaml                            |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_exchange.delegate_mailbox

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 617f723ae16867c609748348                                     |
| uid           | action:sim_exchange:delegate_mailbox                         |
| ref           | sim_exchange.delegate_mailbox                                |
| pack          | sim_exchange                                                 |
| name          | delegate_mailbox                                             |
| description   | Delegate mailbox to different user                           |
| enabled       | True                                                         |
| entry_point   | workflows/delegate_mailbox.yaml                              |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "certificate_file_path": {                               |
|               |         "type": "string",                                    |
|               |         "description": "Certificate file path",              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "default": "Administrator",                          |
|               |         "required": true,                                    |
|               |         "description": "username"                            |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "organisation": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "organisation",                       |
|               |         "default": "etest.systems",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "host": {                                                |
|               |         "type": "string",                                    |
|               |         "description": "host",                               |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com",                              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "user_email": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "User email to act as identify ",     |
|               |         "default": "sim.testuser01@etest.systems",           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "app_id": {                                              |
|               |         "type": "string",                                    |
|               |         "description": "App Id",                             |
|               |         "default": "f9954a04-347a-4a74-be7e-90deceb9ef7a",   |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "delegate_email": {                                      |
|               |         "type": "string",                                    |
|               |         "description": "delegate user email",                |
|               |         "default": "Teams.Test2@etest.systems",              |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/delegate_mailbox.meta.yaml                           |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_exchange.forward_mailbox

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 617f794be16867c60974834c                                     |
| uid           | action:sim_exchange:forward_mailbox                          |
| ref           | sim_exchange.forward_mailbox                                 |
| pack          | sim_exchange                                                 |
| name          | forward_mailbox                                              |
| description   | Delegate mailbox to different user                           |
| enabled       | True                                                         |
| entry_point   | workflows/forward_mailbox.yaml                               |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "certificate_file_path": {                               |
|               |         "type": "string",                                    |
|               |         "description": "Certificate file path",              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "default": "Administrator",                          |
|               |         "required": true,                                    |
|               |         "description": "username"                            |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "organisation": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "organisation",                       |
|               |         "default": "etest.systems",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "host": {                                                |
|               |         "type": "string",                                    |
|               |         "description": "host",                               |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com",                              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "user_email": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "User email to act as identify ",     |
|               |         "default": "sim.testuser01@etest.systems",           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "app_id": {                                              |
|               |         "type": "string",                                    |
|               |         "description": "App Id",                             |
|               |         "default": "f9954a04-347a-4a74-be7e-90deceb9ef7a",   |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "forward_email": {                                       |
|               |         "type": "string",                                    |
|               |         "description": "delegate user email",                |
|               |         "default": "Teams.Test2@etest.systems",              |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/forward_mailbox.meta.yaml                            |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_exchange.get_mailbox_properties

````

+---------------+---------------------------------------------+
| Property      | Value                                       |
+---------------+---------------------------------------------+
| id            | 61820769253cc5f9cb6df1f9                    |
| uid           | action:sim_exchange:get_mailbox_properties  |
| ref           | sim_exchange.get_mailbox_properties         |
| pack          | sim_exchange                                |
| name          | get_mailbox_properties                      |
| description   | Get Mailbox Properties Improved             |
| enabled       | True                                        |
| entry_point   | workflows/get_mailbox_properties.yaml       |
| runner_type   | orquesta                                    |
| parameters    | {                                           |
|               |     "user_email": {                         |
|               |         "type": "string",                   |
|               |         "description": "Email of the user", |
|               |         "required": true                    |
|               |     }                                       |
|               | }                                           |
| metadata_file | actions/get_mailbox_properties.meta.yaml    |
| notify        |                                             |
| output_schema |                                             |
| tags          |                                             |
+---------------+---------------------------------------------+

````

### sim_exchange.user_exit

````

+---------------+-----------------------------------------------+
| Property      | Value                                         |
+---------------+-----------------------------------------------+
| id            | 615a8e9c45844f57d0a5e066                      |
| uid           | action:sim_exchange:user_exit                 |
| ref           | sim_exchange.user_exit                        |
| pack          | sim_exchange                                  |
| name          | user_exit                                     |
| description   | Customer user offboarding orquesta automation |
| enabled       | True                                          |
| entry_point   | workflows/user_exit.yaml                      |
| runner_type   | orquesta                                      |
| parameters    | {                                             |
|               |     "data": {                                 |
|               |         "type": "object",                     |
|               |         "description": "input robot data.",   |
|               |         "required": false                     |
|               |     }                                         |
|               | }                                             |
| metadata_file | actions/user_exit.yaml                        |
| notify        |                                               |
| output_schema |                                               |
| tags          |                                               |
+---------------+-----------------------------------------------+

````

## Prerequisites
These actions use Exchange Online PowerShell V2 module.

Reference - [Authentication for unattended scripts](https://docs.microsoft.com/en-us/powershell/exchange/app-only-auth-powershell-v2?view=exchange-ps)
