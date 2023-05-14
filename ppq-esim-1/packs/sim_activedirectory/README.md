# SiM ActiveDirectory Pack

## Introduction 
This repo holds Ethan SiM Active Directory pack with reusable actions and workflows related to Microsoft Active Directory 
account manipulations.

## Installation 

````
st2 pack install https://ethangroup.visualstudio.com/SPBU%20Automation/_git/sim_activedirectory

````
## Actions and Workflows

The following actions and workflows make up the pack ("`sim-activedirectory`"):

````
+------------------------------------------------+---------------------+-----------------------------------------------+
| ref                                            | pack                | description                                   |
+------------------------------------------------+---------------------+-----------------------------------------------+
| sim_activedirectory.change_description_ad_user | sim_activedirectory | Update description of an AD user              |
| sim_activedirectory.change_ou_ad_user          | sim_activedirectory | Change OU of an AD user                       |
| sim_activedirectory.change_pwd_ad_user         | sim_activedirectory | Change password of AD user                    |
| sim_activedirectory.check_ad_user              | sim_activedirectory | verify if user is present on AD               |
| sim_activedirectory.clear_property_ad_user     | sim_activedirectory | Clear Properties of ad user eg Manager        |
| sim_activedirectory.disable_ad_user            | sim_activedirectory | Disable AD user                               |
| sim_activedirectory.fetch_email_object_ad_user | sim_activedirectory | Fetch Email and Object ID of AD User          |
| sim_activedirectory.get_ad_user                | sim_activedirectory | Get AD user properties                        |
| sim_activedirectory.move_ou_ad_user            | sim_activedirectory | Change OU of AD user                          |
| sim_activedirectory.remove_memberships_ad_user | sim_activedirectory | Remove memberships of AD user                 |
| sim_activedirectory.update_description_ad_user | sim_activedirectory | Update description of AD user                 |
| sim_activedirectory.user_exit                  | sim_activedirectory | Customer user offboarding orquesta automation |
+------------------------------------------------+---------------------+-----------------------------------------------+

````
### sim_activedirectory.AD_user_offboarding

````

+---------------+------------------------------------------------+
| Property      | Value                                          |
+---------------+------------------------------------------------+
| id            | 615a8e7345844f57d0a5e05b                       |
| uid           | action:sim_activedirectory:AD_user_offboarding |
| ref           | sim_activedirectory.AD_user_offboarding        |
| pack          | sim_activedirectory                            |
| name          | AD_user_offboarding                            |
| description   | Sample AD offboarding orquesta automation      |
| enabled       | True                                           |
| entry_point   | workflows/AD_user_offboarding.yaml             |
| runner_type   | orquesta                                       |
| parameters    | {                                              |
|               |     "data": {                                  |
|               |         "type": "object",                      |
|               |         "description": "input robot data.",    |
|               |         "required": false                      |
|               |     }                                          |
|               | }                                              |
| metadata_file | actions/AD_user_offboarding.yaml               |
| notify        |                                                |
| output_schema |                                                |
| tags          |                                                |
+---------------+------------------------------------------------+

````

### sim_activedirectory.change_description_ad_user

````

+---------------+-------------------------------------------------------+
| Property      | Value                                                 |
+---------------+-------------------------------------------------------+
| id            | 616f84edc8101de118685a7d                              |
| uid           | action:sim_activedirectory:change_description_ad_user |
| ref           | sim_activedirectory.change_description_ad_user        |
| pack          | sim_activedirectory                                   |
| name          | change_description_ad_user                            |
| description   | Update description of an AD user                      |
| enabled       | True                                                  |
| entry_point   | workflows/change_description_ad_user.yaml             |
| runner_type   | orquesta                                              |
| parameters    |                                                       |
| metadata_file | actions/change_description_ad_user.meta.yaml          |
| notify        |                                                       |
| output_schema |                                                       |
| tags          |                                                       |
+---------------+-------------------------------------------------------+

````

### sim_activedirectory.change_ou_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616ecdc44fb74340a10d131e                                     |
| uid           | action:sim_activedirectory:change_ou_ad_user                 |
| ref           | sim_activedirectory.change_ou_ad_user                        |
| pack          | sim_activedirectory                                          |
| name          | change_ou_ad_user                                            |
| description   | Change OU of an AD user                                      |
| enabled       | False                                                        |
| entry_point   | workflows/change_ou_ad_user.yaml                             |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "AD host to connect to",              |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com",                              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "default": "Administrator",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_cert": {                                     |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not",                     |
|               |         "default": false                                     |
|               |     },                                                       |
|               |     "new_ou": {                                              |
|               |         "type": "string",                                    |
|               |         "description": "New OU to move the user to",         |
|               |         "default": "OU=disabled,DC=accelnomics,DC=com",      |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "objectid": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "objectid to take action on",         |
|               |         "default": "87061b8b-0dbc-4b4f-91aa-8e3edeb9535b",   |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/change_ou_ad_user.meta.yaml                          |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_activedirectory.change_pwd_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616c5887c8101de118685953                                     |
| uid           | action:sim_activedirectory:change_pwd_ad_user                |
| ref           | sim_activedirectory.change_pwd_ad_user                       |
| pack          | sim_activedirectory                                          |
| name          | change_pwd_ad_user                                           |
| description   | Change password of AD user                                   |
| enabled       | True                                                         |
| entry_point   | workflows/change_pwd_ad_user.yaml                            |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "random_text": {                                         |
|               |         "type": "string",                                    |
|               |         "description": "new password",                       |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "Active Directory host",              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "transport to use",                   |
|               |         "required": false,                                   |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_cert": {                                     |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not",                     |
|               |         "default": false                                     |
|               |     },                                                       |
|               |     "objectid": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "Object id to change password of on   |
|               | AD server",                                                  |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/change_pwd_ad_user.meta.yaml                         |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_activedirectory.check_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616bd853c8101de118685934                                     |
| uid           | action:sim_activedirectory:check_ad_user                     |
| ref           | sim_activedirectory.check_ad_user                            |
| pack          | sim_activedirectory                                          |
| name          | check_ad_user                                                |
| description   | verify if user is present on AD                              |
| enabled       | True                                                         |
| entry_point   | workflows/check_ad_user.yaml                                 |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "Active Directory host",              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "display_name": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "Display name to query on AD server", |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "transport to use",                   |
|               |         "required": false,                                   |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_cert": {                                     |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not",                     |
|               |         "default": false                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/check_ad_user.meta.yaml                              |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_activedirectory.clear_property_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616e4535c8101de11868599f                                     |
| uid           | action:sim_activedirectory:clear_property_ad_user            |
| ref           | sim_activedirectory.clear_property_ad_user                   |
| pack          | sim_activedirectory                                          |
| name          | clear_property_ad_user                                       |
| description   | Clear Properties of ad user eg Manager                       |
| enabled       | True                                                         |
| entry_point   | workflows/clear_property_ad_user.yaml                        |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "AD host to connect to",              |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com",                              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "default": "Administrator",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "transport",                          |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_cert": {                                     |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not"                      |
|               |     },                                                       |
|               |     "objectid": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "objectid to clear properties of",    |
|               |         "default": "87061b8b-0dbc-4b4f-91aa-8e3edeb9535b",   |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "properties_to_clear": {                                 |
|               |         "type": "string",                                    |
|               |         "description": "Comma separated list of properties   |
|               | to clear",                                                   |
|               |         "default": "Manager",                                |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/clear_property_ad_user.meta.yaml                     |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_activedirectory.disable_ad_user

````

+---------------+------------------------------------------------------------+
| Property      | Value                                                      |
+---------------+------------------------------------------------------------+
| id            | 616ce986c8101de11868595c                                   |
| uid           | action:sim_activedirectory:disable_ad_user                 |
| ref           | sim_activedirectory.disable_ad_user                        |
| pack          | sim_activedirectory                                        |
| name          | disable_ad_user                                            |
| description   | Disable AD user                                            |
| enabled       | True                                                       |
| entry_point   | workflows/disable_ad_user.yaml                             |
| runner_type   | orquesta                                                   |
| parameters    | {                                                          |
|               |     "ad_host": {                                           |
|               |         "type": "string",                                  |
|               |         "description": "AD host to connect to",            |
|               |         "required": true                                   |
|               |     },                                                     |
|               |     "username": {                                          |
|               |         "type": "string",                                  |
|               |         "description": "username",                         |
|               |         "required": true                                   |
|               |     },                                                     |
|               |     "password": {                                          |
|               |         "type": "string",                                  |
|               |         "required": true,                                  |
|               |         "secret": true                                     |
|               |     },                                                     |
|               |     "objectid": {                                          |
|               |         "type": "string",                                  |
|               |         "description": "objectid to disable on AD server", |
|               |         "required": true                                   |
|               |     },                                                     |
|               |     "transport": {                                         |
|               |         "type": "string",                                  |
|               |         "description": "transport",                        |
|               |         "default": "ntlm"                                  |
|               |     },                                                     |
|               |     "verify_ssl_cert": {                                   |
|               |         "type": "boolean",                                 |
|               |         "description": "use ssl or not",                   |
|               |         "default": null                                    |
|               |     }                                                      |
|               | }                                                          |
| metadata_file | actions/disable_ad_user.meta.yaml                          |
| notify        |                                                            |
| output_schema |                                                            |
| tags          |                                                            |
+---------------+------------------------------------------------------------+

````

### sim_activedirectory.fetch_email_object_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616c2e18c8101de11868593d                                     |
| uid           | action:sim_activedirectory:fetch_email_object_ad_user        |
| ref           | sim_activedirectory.fetch_email_object_ad_user               |
| pack          | sim_activedirectory                                          |
| name          | fetch_email_object_ad_user                                   |
| description   | Fetch Email and Object ID of AD User                         |
| enabled       | True                                                         |
| entry_point   | workflows/fetch_email_object_ad_user.yaml                    |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "Active Directory host",              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "display_name": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "Display name to query on AD server", |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "transport to use",                   |
|               |         "required": false,                                   |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_cert": {                                     |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not",                     |
|               |         "default": false                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/fetch_email_object_ad_user.meta.yaml                 |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_activedirectory.get_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616a495dc8101de1186858af                                     |
| uid           | action:sim_activedirectory:get_ad_user                       |
| ref           | sim_activedirectory.get_ad_user                              |
| pack          | sim_activedirectory                                          |
| name          | get_ad_user                                                  |
| description   | Get AD user properties                                       |
| enabled       | True                                                         |
| entry_point   | workflows/get_ad_user.yaml                                   |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "Active Directory host",              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "display_name": {                                        |
|               |         "type": "string",                                    |
|               |         "description": "Display name to query on AD server", |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "transport to use",                   |
|               |         "required": false,                                   |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_cert": {                                     |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not",                     |
|               |         "default": false                                     |
|               |     },                                                       |
|               |     "properties": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "List of comma separated properties   |
|               | to fetch. By default fetches all",                           |
|               |         "required": false,                                   |
|               |         "default": "*"                                       |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/get_ad_user.meta.yaml                                |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````
### sim_activedirectory.move_ou_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616e62a5c8101de1186859c3                                     |
| uid           | action:sim_activedirectory:move_ou_ad_user                   |
| ref           | sim_activedirectory.move_ou_ad_user                          |
| pack          | sim_activedirectory                                          |
| name          | move_ou_ad_user                                              |
| description   | Change OU of AD user                                         |
| enabled       | True                                                         |
| entry_point   | workflows/move_ou_ad_user.yaml                               |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "AD host to connect to",              |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com",                              |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "default": "Administrator",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_cert": {                                     |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not",                     |
|               |         "default": false                                     |
|               |     },                                                       |
|               |     "objectid": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "objectid to move the OU of",         |
|               |         "default": "87061b8b-0dbc-4b4f-91aa-8e3edeb9535b",   |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "new_ou": {                                              |
|               |         "type": "string",                                    |
|               |         "description": "new ou to move the AD user to",      |
|               |         "default": "OU=disabled,DC=accelnomics,DC=com",      |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/move_ou_ad_user.meta.yaml                            |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_activedirectory.remove_memberships_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616d177ec8101de11868596f                                     |
| uid           | action:sim_activedirectory:remove_memberships_ad_user        |
| ref           | sim_activedirectory.remove_memberships_ad_user               |
| pack          | sim_activedirectory                                          |
| name          | remove_memberships_ad_user                                   |
| description   | Remove memberships of AD user                                |
| enabled       | True                                                         |
| entry_point   | workflows/remove_memberships_ad_user.yaml                    |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "username": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "username",                           |
|               |         "default": "Administrator",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "required": true,                                    |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "objectid": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "objectid",                           |
|               |         "default": "87061b8b-0dbc-4b4f-91aa-8e3edeb9535b",   |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "transport",                          |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_certs": {                                    |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not",                     |
|               |         "default": null                                      |
|               |     },                                                       |
|               |     "ad_host": {                                             |
|               |         "type": "string",                                    |
|               |         "description": "AD host to connect to",              |
|               |         "default": "ec2-35-154-52-226.ap-                    |
|               | south-1.compute.amazonaws.com",                              |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/remove_memberships_ad_user.meta.yaml                 |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_activedirectory.update_description_ad_user

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 616d02fbc8101de11868596e                                     |
| uid           | action:sim_activedirectory:update_description_ad_user        |
| ref           | sim_activedirectory.update_description_ad_user               |
| pack          | sim_activedirectory                                          |
| name          | update_description_ad_user                                   |
| description   | Update description of AD user                                |
| enabled       | True                                                         |
| entry_point   | workflows/update_description_ad_user.yaml                    |
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
|               |         "default": "Administrator",                          |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "password": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "password",                           |
|               |         "default": "Eth@nGroup12345",                        |
|               |         "secret": true                                       |
|               |     },                                                       |
|               |     "objectid": {                                            |
|               |         "type": "string",                                    |
|               |         "description": "objectid to change description of",  |
|               |         "default": "87061b8b-0dbc-4b4f-91aa-8e3edeb9535b",   |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "transport": {                                           |
|               |         "type": "string",                                    |
|               |         "description": "transport",                          |
|               |         "default": "ntlm"                                    |
|               |     },                                                       |
|               |     "verify_ssl_cert": {                                     |
|               |         "type": "boolean",                                   |
|               |         "description": "use ssl or not",                     |
|               |         "default": false                                     |
|               |     },                                                       |
|               |     "new_description": {                                     |
|               |         "type": "string",                                    |
|               |         "description": "New description to update for AD     |
|               | user",                                                       |
|               |         "default": "Offboarded as part of ticket number      |
|               | 123456",                                                     |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/update_description_ad_user.meta.yaml                 |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_activedirectory.user_exit

````

+---------------+-----------------------------------------------+
| Property      | Value                                         |
+---------------+-----------------------------------------------+
| id            | 615a8e7345844f57d0a5e05e                      |
| uid           | action:sim_activedirectory:user_exit          |
| ref           | sim_activedirectory.user_exit                 |
| pack          | sim_activedirectory                           |
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
## Pre-requisites

Credentials of an administrative user with the requisite authorization to perform the active directory tasks.
Access to an Admin host or the domain controller from the SiM instance . 
