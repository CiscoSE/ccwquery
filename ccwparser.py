from pprint import pprint
import json




class CCWOrderParser(object):

    def __init__(self,variable):

        """
        init - This init method is called whenever a new object is instantiated.   This will take the the raw text
               from CCW Output and parse the appropriate data from the records into the appropriate fields.
        :return: nothing
        """


        self.rawdata = variable
        self.jsondata = json.loads(variable)

        headerlocation = self.jsondata['ShowPurchaseOrder']['value']['DataArea']['PurchaseOrder'][0]['PurchaseOrderHeader']

        self.billtoparty = headerlocation['BillToParty']['Name'][0]['value']
        self.party = headerlocation['Party'][0]['Name'][0]['value']
        self.status = headerlocation['Status'][0]['Description']['value']
        self.salesordernum = headerlocation['SalesOrderReference'][0]['ID']['value']
        self.shiptoparty = headerlocation['ShipToParty']['Name'][0]['value']

        self.amount = headerlocation['TotalAmount']['value']
        self.currencycode = headerlocation['TotalAmount']['currencyCode']

        self.linelocation = self.jsondata['ShowPurchaseOrder']['value']['DataArea']['PurchaseOrder'][0]['PurchaseOrderLine']

        self.orderdetail = []
        for i in self.linelocation:

            line = {"sku": i['Item']['ID']['value'],
                    "description": i['Item']['Description'][0]['value'],
                    "quantity": i['Item']['Lot'][0]['Quantity']['value'],
                    "line": i['SalesOrderReference']['LineNumberID']['value'],
                    "amount": i['ExtendedAmount']['value']
                    }
            self.orderdetail.append(line)



    def display(self):
        """
        dispay - This method will display the raw json in pretty print format
        :return: nothing
        """
        pprint(self.jsondata)


    def status(self):
        """
        status - This method provides access to the status
        :return: status (String)
        """
        return self.status

    def billtoparty(self):
        """
        billtoparty - This method provides access to the bill-to-party
        :return: billtoparty (String)
        """
        return self.billtoparty

    def party(self):
        """
        party - This method provides access to the party (Seems to be the end customer)
        :return: party (String)
        """
        return self.party

    def salesordernum(self):
        """
        salesordernum - This method provides access to the sales order number (SO#)
        :return: salesordernum (String)
        """
        return self.salesordernum

    def shiptoparty(self):
        """
        shiptoparty - This method provides access to the ship-to-party (Where the equipment is shipped)
        :return: shiptoparty (String)
        """
        return self.shiptoparty

    def amount(self):
        """
        amount - This method provides access to the total amount of the order
        :return: amount (Float)
        """
        return self.amount

    def currencycode(self):
        """
        currencycode - This method provides access to the currency code of the oder
        :return: currencycode (String)
        """
        return self.currencycode

    def linelocation(self):
        return self.linelocation


    def orderdetail(self):
        """
        orderdetail - This method will return the dictionary that represents the details of the order.
        :return: orderdetail (Dictionary)
        """
        return self.orderdetail


    def display_order_detail(self,displaytoplevel=False):
        """
        display_order_detail - This method will display to the screen the details of the line items of the order.

        :param displaytoplevel: This parameter specifies if we want to only display the top order part number
                as opposed to all the sub line items.
        :return: none
        """

        message = "{:5}   {:5}    {:20}     {:80} {:10}\n".format("Line","Qty","Sku","Description","Amount")
        message = message+"{:5}   {:5}    {:20}     {:80} {:10}\n".format("-----","-----","--------------------",
                                                            "-----------------------------------------------------",
                                                            "----------")

        for i in self.orderdetail:

            printline = True
            if (displaytoplevel) and (i['line'].find(".0") < 0):
                printline = False
            if printline:
                message=message+ "{:<5}   {:<5}    {:<20}     {:<80} {:>10.2f}\n".format(i['line'], str(i['quantity']), i['sku'],
                                                                            i['description'], i['amount'])

        return message