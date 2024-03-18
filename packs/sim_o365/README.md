# SiM O365 Pack

## Introduction 
sim_o365 pack supplies actions for services related to Microsoft Office 365 to be used with the SiM platform.

## Installing the pack

````

st2 pack install https://ethangroup.visualstudio.com/SPBU%20Automation/_git/sim_o365


````

## Actions and Workflows

The following actions and workflows make up the pack ("`sim-o365`"):

````

+-------------------------------+----------+-------------------------------------------------+
| ref                           | pack     | description                                     |
+-------------------------------+----------+-------------------------------------------------+
| sim_o365.block_user_signin    | sim_o365 | Block the user from signing in                  |
| sim_o365.get_graphapi_token   | sim_o365 | Get access token from Microsoft Graph API       |
| sim_o365.get_user_licenses    | sim_o365 | Get user licenses from office365 Admin centre:  |
| sim_o365.hide_address_gal     | sim_o365 | Hide address from Global Address list using     |
|                               |          | Microsoft Graph API                             |
| sim_o365.remove_user_licenses | sim_o365 | Remove User Licenses                            |
+-------------------------------+----------+-------------------------------------------------+

````

### sim_o365.AD_user_offboarding

````

+---------------+---------------------------------------------+
| Property      | Value                                       |
+---------------+---------------------------------------------+
| id            | 615a8f0345844f57d0a5e06b                    |
| uid           | action:sim_o365:AD_user_offboarding         |
| ref           | sim_o365.AD_user_offboarding                |
| pack          | sim_o365                                    |
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

### sim_o365.Test_User_Licenses

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 61713925c8101de118685c3d                                     |
| uid           | action:sim_o365:Test_User_Licenses                           |
| ref           | sim_o365.Test_User_Licenses                                  |
| pack          | sim_o365                                                     |
| name          | Test_User_Licenses                                           |
| enabled       | True                                                         |
| entry_point   | workflows/Test_User_Licenses.yaml                            |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "graph_auth_token": {                                    |
|               |         "type": "string",                                    |
|               |         "description": "graph_auth_token",                   |
|               |         "default": "eyJ0eXAiOiJKV1QiLCJub25jZSI6IkF5blJ6VGdt |
|               | Q1R5V1B3NGNEbTVJUlFpVy1YV3QwZWdnTVc4TXQ2bWI5N2MiLCJhbGciOiJS |
|               | UzI1NiIsIng1dCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCIsImtp |
|               | ZCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCJ9.eyJhdWQiOiJodHR |
|               | wczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy5 |
|               | 3aW5kb3dzLm5ldC9iMDJlNTBhYy0yMGU1LTRjNjAtYmNkNC04NDU0YjMyMDF |
|               | mZDEvIiwiaWF0IjoxNjM0ODExMTU1LCJuYmYiOjE2MzQ4MTExNTUsImV4cCI |
|               | 6MTYzNDgxNTA1NSwiYWlvIjoiRTJaZ1lGRDdWdGg3Zm9ML3oxMXVxeFZPVEd |
|               | IN0FBQT0iLCJhcHBfZGlzcGxheW5hbWUiOiJTaU0gR3JhcGggQVBJIEludGV |
|               | ncmF0aW9uIiwiYXBwaWQiOiIwY2UyNzBkMi1jMjUzLTQ1NGUtYmM3Zi1hOTU |
|               | 4NzdmNTRjOWYiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy5 |
|               | 3aW5kb3dzLm5ldC9iMDJlNTBhYy0yMGU1LTRjNjAtYmNkNC04NDU0YjMyMDF |
|               | mZDEvIiwiaWR0eXAiOiJhcHAiLCJvaWQiOiJmZjA5YWQ4Yy03MDVhLTQxNjY |
|               | tYmY3NS0xYTMyZjAzZmY3ZDkiLCJyaCI6IjAuQVdjQXJGQXVzT1VnWUV5ODF |
|               | JUlVzeUFmMGRKdzRneFR3azVGdkgtcFdIZjFUSjluQUFBLiIsInJvbGVzIjp |
|               | bIlVzZXIuUmVhZFdyaXRlLkFsbCJdLCJzdWIiOiJmZjA5YWQ4Yy03MDVhLTQ |
|               | xNjYtYmY3NS0xYTMyZjAzZmY3ZDkiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjo |
|               | iT0MiLCJ0aWQiOiJiMDJlNTBhYy0yMGU1LTRjNjAtYmNkNC04NDU0YjMyMDF |
|               | mZDEiLCJ1dGkiOiJhWGhySVVoNzUwZUlkNUVsb0UxU0FRIiwidmVyIjoiMS4 |
|               | wIiwid2lkcyI6WyIwOTk3YTFkMC0wZDFkLTRhY2ItYjQwOC1kNWNhNzMxMjF |
|               | lOTAiXSwieG1zX3RjZHQiOjE1NTIyOTA2MjZ9.WEH_iujtPIXbK09c6OuJ-N |
|               | SP0vRifhIeHY1nv1XSpAAqOvxIwfJCLg0Lg_fNYtZuL7HWvyvXZnUcGz4Stl |
|               | cAqm9Zvbf9UCHRpGyqH_MUJXDE3gL8979XPvOk6bDe0luQkPD6ROOQWhtFMT |
|               | vofr4Sij3tYel66itpHbVSvt_PAz8Vkg0S4ZLzb82UoY_ysio5H2a_XZ5Sof |
|               | rNFCunYq-mp4ptQUIZTtynNGR7WY0KAJ2Yq75HmJZK4njmzh-            |
|               | XG3Cl423ZhZ3uqa2hjZm8-c5u5TURi52KfXCKzYW2sxJqolwP-           |
|               | oArlkxQ9VlStlZKEWGAyP232ZZmJyXd851et4dwnA",                  |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "user_email": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "user_email",                         |
|               |         "default": "sim.testuser01@etest.systems",           |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "new_parameter": {                                       |
|               |         "type": "string"                                     |
|               |     },                                                       |
|               |     "one_more_new_parameter": {                              |
|               |         "type": "string"                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/Test_User_Licenses.meta.yaml                         |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_o365.block_user_signin

````

+---------------+----------------------------------------------------+
| Property      | Value                                              |
+---------------+----------------------------------------------------+
| id            | 61704d02c8101de118685b83                           |
| uid           | action:sim_o365:block_user_signin                  |
| ref           | sim_o365.block_user_signin                         |
| pack          | sim_o365                                           |
| name          | block_user_signin                                  |
| description   | Block the user from signing in                     |
| enabled       | True                                               |
| entry_point   | workflows/block_user_signin.yaml                   |
| runner_type   | orquesta                                           |
| parameters    | {                                                  |
|               |     "user_email": {                                |
|               |         "type": "string",                          |
|               |         "description": "User Email",               |
|               |         "default": "sim.testuser01@etest.systems", |
|               |         "required": true                           |
|               |     },                                             |
|               |     "graph_auth_token": {                          |
|               |         "type": "string",                          |
|               |         "description": "Graph API token",          |
|               |         "required": true                           |
|               |     }                                              |
|               | }                                                  |
| metadata_file | actions/block_user_signin.meta.yaml                |
| notify        |                                                    |
| output_schema |                                                    |
| tags          |                                                    |
+---------------+----------------------------------------------------+

````

### sim_o365.get_graphapi_token

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 61704085c8101de118685b6d                                     |
| uid           | action:sim_o365:get_graphapi_token                           |
| ref           | sim_o365.get_graphapi_token                                  |
| pack          | sim_o365                                                     |
| name          | get_graphapi_token                                           |
| description   | Get access token from Microsoft Graph API                    |
| enabled       | True                                                         |
| entry_point   | workflows/get_graphapi_token.yaml                            |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "tenant_id": {                                           |
|               |         "type": "string",                                    |
|               |         "default": "b02e50ac-20e5-4c60-bcd4-8454b3201fd1",   |
|               |         "description": "Tenant ID for Microsoft Graph API",  |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "client_id": {                                           |
|               |         "default": "0ce270d2-c253-454e-bc7f-a95877f54c9f",   |
|               |         "type": "string",                                    |
|               |         "description": "client ID for microsoft graph API",  |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "client_secret": {                                       |
|               |         "type": "string",                                    |
|               |         "description": "Client secret for Microsoft graph    |
|               | API",                                                        |
|               |         "default": "APu7Q~jD_UGTgQWl~1H2kQBgtitmYyHuzXNmj",  |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/get_graphapi_token.meta.yaml                         |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_o365.get_user

````

+---------------+------------------------------------------------+
| Property      | Value                                          |
+---------------+------------------------------------------------+
| id            | 617d33b5e436c412be8fc5a0                       |
| uid           | action:sim_o365:get_user                       |
| ref           | sim_o365.get_user                              |
| pack          | sim_o365                                       |
| name          | get_user                                       |
| description   | Get User Properties from O365                  |
| enabled       | True                                           |
| entry_point   | workflows/get_user.yaml                        |
| runner_type   | orquesta                                       |
| parameters    | {                                              |
|               |     "user_email": {                            |
|               |         "type": "string",                      |
|               |         "description": "User email",           |
|               |         "required": true                       |
|               |     },                                         |
|               |     "graph_auth_token": {                      |
|               |         "type": "string",                      |
|               |         "description": "Graph API auth token", |
|               |         "required": true                       |
|               |     }                                          |
|               | }                                              |
| metadata_file | actions/get_user.meta.yaml                     |
| notify        |                                                |
| output_schema |                                                |
| tags          |                                                |
+---------------+------------------------------------------------+

````

### sim_o365.get_user_licenses

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 61705593c8101de118685b87                                     |
| uid           | action:sim_o365:get_user_licenses                            |
| ref           | sim_o365.get_user_licenses                                   |
| pack          | sim_o365                                                     |
| name          | get_user_licenses                                            |
| description   | Get user licenses from office365 Admin centre:               |
| enabled       | True                                                         |
| entry_point   | workflows/get_user_licenses.yaml                             |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "graph_auth_token": {                                    |
|               |         "type": "string",                                    |
|               |         "description": "Graph API auth token",               |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "user_email": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "User Email Address to get licenses   |
|               | of",                                                         |
|               |         "required": true,                                    |
|               |         "default": "sim.testuser01@etest.systems"            |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/get_user_licenses.meta.yaml                          |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_o365.hide_address_gal

````

+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 61704655c8101de118685b7a                                     |
| uid           | action:sim_o365:hide_address_gal                             |
| ref           | sim_o365.hide_address_gal                                    |
| pack          | sim_o365                                                     |
| name          | hide_address_gal                                             |
| description   | Hide address from Global Address list using Microsoft Graph  |
|               | API                                                          |
| enabled       | True                                                         |
| entry_point   | workflows/hide_address_gal.yaml                              |
| runner_type   | orquesta                                                     |
| parameters    | {                                                            |
|               |     "user_email": {                                          |
|               |         "type": "string",                                    |
|               |         "description": "User email to hide from GAL",        |
|               |         "required": true,                                    |
|               |         "default": "sim.testuser01@etest.systems"            |
|               |     },                                                       |
|               |     "graph_auth_token": {                                    |
|               |         "type": "string",                                    |
|               |         "description": "Graph API auth token",               |
|               |         "required": true                                     |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/hide_address_gal.meta.yaml                           |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+

````

### sim_o365.remove_user_licenses

````

+---------------+----------------------------------------------------+
| Property      | Value                                              |
+---------------+----------------------------------------------------+
| id            | 61705c44c8101de118685b94                           |
| uid           | action:sim_o365:remove_user_licenses               |
| ref           | sim_o365.remove_user_licenses                      |
| pack          | sim_o365                                           |
| name          | remove_user_licenses                               |
| description   | Remove User Licenses                               |
| enabled       | True                                               |
| entry_point   | workflows/remove_user_licenses.yaml                |
| runner_type   | orquesta                                           |
| parameters    | {                                                  |
|               |     "user_email": {                                |
|               |         "type": "string",                          |
|               |         "description": "User Email",               |
|               |         "default": "sim.testuser01@etest.systems", |
|               |         "required": true                           |
|               |     },                                             |
|               |     "graph_auth_token": {                          |
|               |         "type": "string",                          |
|               |         "description": "Graph API token",          |
|               |         "required": true                           |
|               |     },                                             |
|               |     "licenses": {                                  |
|               |         "type": "array",                           |
|               |         "description": "Licenses list",            |
|               |         "required": true                           |
|               |     }                                              |
|               | }                                                  |
| metadata_file | actions/remove_user_licenses.meta.yaml             |
| notify        |                                                    |
| output_schema |                                                    |
| tags          |                                                    |
+---------------+----------------------------------------------------+

````
### sim_o365.user_exit

````

+---------------+-----------------------------------------------+
| Property      | Value                                         |
+---------------+-----------------------------------------------+
| id            | 615a8f0345844f57d0a5e06e                      |
| uid           | action:sim_o365:user_exit                     |
| ref           | sim_o365.user_exit                            |
| pack          | sim_o365                                      |
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

### sim_o365.user_offboarding_exchange_o365

````

+---------------+-------------------------------------------------------------+
| Property      | Value                                                       |
+---------------+-------------------------------------------------------------+
| id            | 617599c7cef832a22c4147e6                                    |
| uid           | action:sim_o365:user_offboarding_exchange_o365              |
| ref           | sim_o365.user_offboarding_exchange_o365                     |
| pack          | sim_o365                                                    |
| name          | user_offboarding_exchange_o365                              |
| description   | CCDBB User Offboarding exchange for O365                    |
| enabled       | True                                                        |
| entry_point   | workflows/user_offboarding_exchange_o365.yaml               |
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
|               |     }                                                       |
|               | }                                                           |
| metadata_file | actions/user_offboarding_exchange_o365.meta.yaml            |
| notify        |                                                             |
| output_schema |                                                             |
| tags          |                                                             |
+---------------+-------------------------------------------------------------+

````

### sim_o365.user_offboarding_o365

````

+---------------+-----------------------------------------+
| Property      | Value                                   |
+---------------+-----------------------------------------+
| id            | 61759955cef832a22c4147e5                |
| uid           | action:sim_o365:user_offboarding_o365   |
| ref           | sim_o365.user_offboarding_o365          |
| pack          | sim_o365                                |
| name          | user_offboarding_o365                   |
| description   | CCDBB User Offboarding for O365         |
| enabled       | True                                    |
| entry_point   | workflows/user_offboarding_o365.yaml    |
| runner_type   | orquesta                                |
| parameters    |                                         |
| metadata_file | actions/user_offboarding_o365.meta.yaml |
| notify        |                                         |
| output_schema |                                         |
| tags          |                                         |
+---------------+-----------------------------------------+

````

## Prerequisites
The actions use the Microsoft Graph APIs. Hence, applciation secret/access token with correct permissions is required for these actions to work.
