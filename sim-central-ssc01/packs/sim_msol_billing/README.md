# SiM MSOL Pack

## Introduction
sim_msol pack supplies actions for services related to Microsoft Online to be used with the SiM platform.

## Installing the pack

````

st2 pack install https://ethangroup.visualstudio.com/SPBU%20Automation/_git/sim_msol


````

## Actions and Workflows

The following actions and workflows make up the pack ("`sim_msol`"):

````

+----------------------------------------------+----------+-------------------------------------------------+
| ref                                          | pack     | description                                     |
+----------------------------------------------+----------+-------------------------------------------------+
| sim_msol.place_msol_order                    | sim_msol | Place Order on Microsoft Online                 |
| sim_msol.place_msol_order_from_offer_id      | sim_msol | Place Order on Microsoft Online from Offer ID   |
| sim_msol.place_msol_order_from_product_title | sim_msol | Place Order on Microsoft Online from Product    |
|                                              |          | Title                                           |
+----------------------------------------------+----------+-------------------------------------------------+

````

## Prerequisites
The actions use the Microsoft Online Partner Center APIs. Hence, application secret/access token with correct permissions is required for these actions to work.

