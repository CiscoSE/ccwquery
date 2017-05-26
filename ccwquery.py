import requests
import json
from pprint import pprint
import ccwparser
import ConfigParser




def get_access_token(client_id, client_secret, username, password):

    grant_type = "password"
    url = "https://cloudsso.cisco.com/as/token.oauth2"
    payload = "client_id="+client_id+ \
              "&client_secret="+client_secret+ \
              "&username="+username+ \
              "&grant_type=password&password="+password


#    payload = "client_id="+client_id+"&grant_type=client_credentials&client_secret="+client_secret

    print payload


    headers = {
        'accept': "application/json",
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    if (response.status_code == 200):
        return response.json()['access_token']
    else:
        response.raise_for_status()



def get_order_details(access_token,id,id_type="WO"):

    if (id_type == "WO"):
        wo_id = id
        so_id = ""

    elif (id_type == "SO"):
        wo_id = ""
        so_id =id

    print "WO ID  = "+wo_id
    print "SO ID  = "+so_id


    payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n" \
              "<GetPurchaseOrder xmlns=\"http://www.openapplications.org/oagis/10\">\r\n\r\n " \
              "<ApplicationArea>\r\n " \
              "<CreationDateTime>datetime</CreationDateTime>\r\n " \
              "</ApplicationArea>\r\n \r\n " \
              "<DataArea>\r\n \r\n " \
              "<PurchaseOrder>\r\n " \
              "<PurchaseOrderHeader>\r\n " \
              "<ID></ID>\r\n \r\n\t\t" \
              "<DocumentReference>\r\n\t\t\t" \
              "<ID>"+wo_id+ \
              "</ID>\r\n\t\t\t\r\n\t\t" \
              "</DocumentReference>\r\n\t\t" \
              "<SalesOrderReference>\r\n\t\t\t<ID>"+so_id+ \
              "</ID>\r\n\t\t\t\r\n\t\t" \
              "</SalesOrderReference>\r\n\t\t\r\n\t\t" \
              "<Description typeCode=\"details\">YES</Description>\r\n " \
              "</PurchaseOrderHeader>\r\n " \
              "</PurchaseOrder>\r\n \r\n " \
              "</DataArea>\r\n \r\n" \
              "</GetPurchaseOrder>"

    url = "https://api.cisco.com/commerce/ORDER/v2/sync/checkOrderStatus"
    headers = {
        'authorization': "Bearer " + access_token,
        'accept': "application/json",
        'content-type': "application/xml",
        'x-mashery-message-id': "TESTID1239",
        'cache-control': "no-cache"
    }

    print headers

    response = requests.request("POST", url, data=payload, headers=headers)

    print response

    if (response.status_code == 200):
        # Uncomment to debug
#        sys.stderr.write(response.text)

        print response.text



        # Check if case was found
#        if response.json()['RESPONSE']['COUNT'] == 1:
#            return response.json()
#        else:
#            return False
        return response.text
    else:
        response.raise_for_status()
        return""

########################
########################
########################
print "CCW Query Engine Starting...\n"

# Open up the configuration file and get all application defaults
config = ConfigParser.ConfigParser()
config.read('package_config.ini')

try:
    client_id = config.get("application","client_id")
    client_secret = config.get("application","client_secret")
    username = config.get("application","username")
    password = config.get("application","password")

except ConfigParser.NoOptionError:
    print "package_config.ini is not formatted approriately"
    exit()
except:
    print "Unexpected Error"
    exit()


access_token = get_access_token(client_id,client_secret,username,password)

print access_token

ordernum = input("Enter a Cisco Sales Order Number: ")
order_text = get_order_details(access_token, str(ordernum))

print order_text



order=ccwparser.CCWOrderParser(order_text)
order.display()

print "Displaying information for SO#"+order.salesordernum

print "Party: "+order.party
print "Bill To Party: "+order.billtoparty
print "Ship To Party: "+order.shiptoparty
print "Current Status: "+order.status
print "Total Amount: "+str(order.amount) + " "+order.currencycode


print "Order Details"
print "============="
print order.display_order_detail()