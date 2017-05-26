# ccwquery
Simple Query Application for Cisco Commerce Workspace

## Usage
This application leverages an object oriented approach to parse through a sales order from CCW.

* ccwparser.py - Implementation of the CCWOrderParser Class
* ccwquery.py - Implementation of a test application to use the class

## Requirements
This application requires access to the "CCW Order API" provided at [https://apiconsole.cisco.com/](https://apiconsole.cisco.com/)

You will need to register for an account.   This will allow you to request access to the API which allows you to query for Cisco Access.

ccwquery.py is a very basic application that is used to request the sales order details using the Cisco API.   This can be used as an example for your own  code.

## Methods Implemented
* __init__ - Initalizer for the object.   You initialize the class by something similar to the following: ```order=ccwparser.CCWOrderParser(order_text)```
This example will take the raw text returned from the CCW API Request.   It will convert it to JSON, and then set up the internal variables
* display() - This will return the order in pprint format
* status() - This will return the status of the order
* billtoparty() - This will return the bill to party of the order
* party() - This will return the party of the order (Most likely the end customer)
* salesordernum() - This will return the Sales Order Number (SO#)
* shiptoparty() - This will return the ship to party of the order
* amount() - This will return the total amount of the order
* currencycode() - This will return the currency code used for teh order
* orderdetail() - This will return a dictionary of the order
* display_order_detail() - This will return the details of the order in a very pretty format



