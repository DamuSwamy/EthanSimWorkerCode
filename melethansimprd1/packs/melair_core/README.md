# CCDBB Core Pack

## Introduction 

This repo holds CCDBB client specific integrations/automations/workflows. 

## Installation

````
st2 pack install https://ethangroup.visualstudio.com/SPBU%20Automation/_git/ccdbb_core

````

## Actions and Workflows

The following actions and workflows make up the pack ("`ccdbb-core`"):
````
+-------------------------------------------+------------+---------------------------------------------------+
| ref                                       | pack       | description                                       |
+-------------------------------------------+------------+---------------------------------------------------+
| ccdbb_core.get_user_status                | ccdbb_core | Get Before Automation Status of User              |
| ccdbb_core.offboard_user                  | ccdbb_core | Offboard CCDBB user                               |
| ccdbb_core.user_offboard_activedirectory  | ccdbb_core | Active directory steps for CCDBB user offboarding |
| ccdbb_core.user_offboard_exchange_o365    | ccdbb_core | CCDBB User Offboarding exchange for O365          |
| ccdbb_core.user_offboard_exchange_process | ccdbb_core | CCDBB User Offboarding Exchange Procedure         |
| ccdbb_core.user_offboard_o365_licenses    | ccdbb_core | CCDBB user offboarding O365 licenses and block    |
+-------------------------------------------+------------+---------------------------------------------------+

````

### ccdbb_core.get_user_status

````
+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 6180ee8ed1e64da7c9c8d463                                     |
| uid           | action:ccdbb_core:get_user_status                            |
| ref           | ccdbb_core.get_user_status                                   |
| pack          | ccdbb_core                                                   |
| name          | get_user_status                                              |
| description   | Get Before Automation Status of User                         |
| enabled       | True                                                         |
| entry_point   | workflows/get_user_status.yaml                               |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "AD host to connect to",              |
|               |         "required": true,                                    |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com"                               |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "required": true,                                    |
|               |         "default": "Administrator"                           |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "Password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "display_name": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "Display User to get properties of",  |
|               |         "required": true,                                    |
|               |         "default": "SiM Test User"                           |
|               |     },                                                       |
|               |     "client_id": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "Client ID for graph API token",      |
|               |         "required": true,                                    |
|               |         "default": "0ce270d2-c253-454e-bc7f-a95877f54c9f"    |
|               |     },                                                       |
|               |     "client_secret": {                                       |
|               |         "type": "string",                                    |
|               |         "description": "Client secret for Graph API",        |
|               |         "required": true,                                    |
|               |         "default": "APu7Q~jD_UGTgQWl~1H2kQBgtitmYyHuzXNmj"   |
|               |     },                                                       |
|               |     "tenant_id": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "Tenant ID for Graph API",            |
|               |         "required": true,                                    |
|               |         "default": "b02e50ac-20e5-4c60-bcd4-8454b3201fd1"    |
|               |     },                                                       |
|               |     "when": {                                                |
|               |         "type": "string",                                    |
|               |         "description": "Before or After",                    |
|               |         "default": "Before",                                 |
|               |         "required": false                                    |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/get_user_status.yaml                                 |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### ccdbb_core.offboard_user

````
+---------------+----------------------------------------------+
| Property      | Value                                        |
+---------------+----------------------------------------------+
| id            | 61761f2dad30bfe516a104ce                     |
| uid           | action:ccdbb_core:offboard_user              |
| ref           | ccdbb_core.offboard_user                     |
| pack          | ccdbb_core                                   |
| name          | offboard_user                                |
| description   | Offboard CCDBB user                          |
| enabled       | True                                         |
| entry_point   | workflows/offboard_user.yaml                 |
| runner_type   | orquesta                                     |
| parameters    | {                                            |
|               |     "data": {                                |
|               |         "type": "object",                    |
|               |         "description": "Input json payload", |
|               |         "required": true                     |
|               |     }                                        |
|               | }                                            |
| metadata_file | actions/offboard_user.meta.yaml              |
| notify        |                                              |
| output_schema |                                              |
| tags          |                                              |
+---------------+----------------------------------------------+

````

### ccdbb_core.user_offboard_activedirectory

````
+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 6180edd46cb73c360632fdf3                                     |
| uid           | action:ccdbb_core:user_offboard_activedirectory              |
| ref           | ccdbb_core.user_offboard_activedirectory                     |
| pack          | ccdbb_core                                                   |
| name          | user_offboard_activedirectory                                |
| description   | Active directory steps for CCDBB user offboarding            |
| enabled       | True                                                         |
| entry_point   | workflows/user_offboard_activedirectory.yaml                 |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "AD host to connect to",              |
|               |         "required": true,                                    |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com"                               |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "required": true,                                    |
|               |         "default": "Administrator"                           |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "required": true,                                    |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "display_user": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "Display name of AD User to           |
|               | off_board",                                                  |
|               |         "required": true,                                    |
|               |         "default": "SiM Test User"                           |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/user_offboard_activedirectory.meta.yaml              |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### ccdbb_core.user_offboard_exchange_o365

````

+---------------+-------------------------------------------------------------+
| Property      | Value                                                       |
+---------------+-------------------------------------------------------------+
| id            | 6180edd46cb73c360632fdf4                                    |
| uid           | action:ccdbb_core:user_offboard_exchange_o365               |
| ref           | ccdbb_core.user_offboard_exchange_o365                      |
| pack          | ccdbb_core                                                  |
| name          | user_offboard_exchange_o365                                 |
| description   | CCDBB User Offboarding exchange for O365                    |
| enabled       | True                                                        |
| entry_point   | workflows/user_offboard_exchange_o365.yaml                  |
| runner_type   | orquesta                                                    |
| parameters    | {                                                           |
|               |     "client_id": {                                          |
|               |         "type": "string",                                   |
|               |         "description": "Client ID",                         |
|               |         "default": "0ce270d2-c253-454e-bc7f-a95877f54c9f",  |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "client_secret": {                                      |
|               |         "type": "string",                                   |
|               |         "description": "client_secret for graph api",       |
|               |         "default": "APu7Q~jD_UGTgQWl~1H2kQBgtitmYyHuzXNmj", |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "tenant_id": {                                          |
|               |         "type": "string",                                   |
|               |         "description": "Tenant id",                         |
|               |         "default": "b02e50ac-20e5-4c60-bcd4-8454b3201fd1",  |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "user_email": {                                         |
|               |         "type": "string",                                   |
|               |         "default": "sim.testuser01@etest.systems",          |
|               |         "required": true                                    |
|               |     }                                                       |
|               | }                                                           |
| metadata_file | actions/user_offboard_exchange_o365.meta.yaml               |
| notify        |                                                             |
| output_schema |                                                             |
| tags          |                                                             |
+---------------+-------------------------------------------------------------+

````
### ccdbb_core.user_offboard_exchange_process

````
+---------------+-------------------------------------------------------------+
| Property      | Value                                                       |
+---------------+-------------------------------------------------------------+
| id            | 6180edd46cb73c360632fdf4                                    |
| uid           | action:ccdbb_core:user_offboard_exchange_o365               |
| ref           | ccdbb_core.user_offboard_exchange_o365                      |
| pack          | ccdbb_core                                                  |
| name          | user_offboard_exchange_o365                                 |
| description   | CCDBB User Offboarding exchange for O365                    |
| enabled       | True                                                        |
| entry_point   | workflows/user_offboard_exchange_o365.yaml                  |
| runner_type   | orquesta                                                    |
| parameters    | {                                                           |
|               |     "client_id": {                                          |
|               |         "type": "string",                                   |
|               |         "description": "Client ID",                         |
|               |         "default": "0ce270d2-c253-454e-bc7f-a95877f54c9f",  |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "client_secret": {                                      |
|               |         "type": "string",                                   |
|               |         "description": "client_secret for graph api",       |
|               |         "default": "APu7Q~jD_UGTgQWl~1H2kQBgtitmYyHuzXNmj", |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "tenant_id": {                                          |
|               |         "type": "string",                                   |
|               |         "description": "Tenant id",                         |
|               |         "default": "b02e50ac-20e5-4c60-bcd4-8454b3201fd1",  |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "user_email": {                                         |
|               |         "type": "string",                                   |
|               |         "default": "sim.testuser01@etest.systems",          |
|               |         "required": true                                    |
|               |     }                                                       |
|               | }                                                           |
| metadata_file | actions/user_offboard_exchange_o365.meta.yaml               |
| notify        |                                                             |
| output_schema |                                                             |
| tags          |                                                             |
+---------------+-------------------------------------------------------------+

````
### ccdbb_core.user_offboard_o365_licenses

````
+---------------+-------------------------------------------------------------+
| Property      | Value                                                       |
+---------------+-------------------------------------------------------------+
| id            | 6180edd46cb73c360632fdf4                                    |
| uid           | action:ccdbb_core:user_offboard_exchange_o365               |
| ref           | ccdbb_core.user_offboard_exchange_o365                      |
| pack          | ccdbb_core                                                  |
| name          | user_offboard_exchange_o365                                 |
| description   | CCDBB User Offboarding exchange for O365                    |
| enabled       | True                                                        |
| entry_point   | workflows/user_offboard_exchange_o365.yaml                  |
| runner_type   | orquesta                                                    |
| parameters    | {                                                           |
|               |     "client_id": {                                          |
|               |         "type": "string",                                   |
|               |         "description": "Client ID",                         |
|               |         "default": "0ce270d2-c253-454e-bc7f-a95877f54c9f",  |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "client_secret": {                                      |
|               |         "type": "string",                                   |
|               |         "description": "client_secret for graph api",       |
|               |         "default": "APu7Q~jD_UGTgQWl~1H2kQBgtitmYyHuzXNmj", |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "tenant_id": {                                          |
|               |         "type": "string",                                   |
|               |         "description": "Tenant id",                         |
|               |         "default": "b02e50ac-20e5-4c60-bcd4-8454b3201fd1",  |
|               |         "required": true                                    |
|               |     },                                                      |
|               |     "user_email": {                                         |
|               |         "type": "string",                                   |
|               |         "default": "sim.testuser01@etest.systems",          |
|               |         "required": true                                    |
|               |     }                                                       |
|               | }                                                           |
| metadata_file | actions/user_offboard_exchange_o365.meta.yaml               |
| notify        |                                                             |
| output_schema |                                                             |
| tags          |                                                             |
+---------------+-------------------------------------------------------------+

````
