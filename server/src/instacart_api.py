import jwt.utils
import time
import math
import requests
import uuid
import http.client

    
class InstaCart:
    
    
    def findStores(addressLine1, postalCode):
        
        conn = http.client.HTTPSConnection("connect.instacart.com")
        
        payload = "{\n  \"find_by\": {\n    \"address_line_1\": \"" + addressLine1 + "\",\n    \"postal_code\": \"" + postalCode + "\"\n  }\n}"

        headers = {
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Authorization': "Bearer <token>"
            }

        conn.request("POST", "/v2/fulfillment/stores/delivery", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        
        return data
    
    def createConnectUser(user_id, first_name, last_name):
        conn = http.client.HTTPSConnection("connect.instacart.com")

        payload = "{\n  \"user_id\": \"" + user_id + "\",\n  \"first_name\": \"" + first_name + "\",\n  \"last_name\": \"" + last_name + "\"\n}"

        headers = {
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Authorization': "Bearer <token>"
            }

        conn.request("POST", "/v2/fulfillment/users", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        
        return data
    
    # \"line_num\": \"string\",\n      \"count\": 1,\n      \"weight\": 1,\n      \"special_instructions\": \"string\",\n      \"replacement_policy\": \"no_replacements\",\n      \"replacement_items\": [\n        {\n          \"upc\": \"string\"\n        }\n      ],\n      \"item\": {\n        \"upc\": \"string\"\n      }\n    }\n
    def itemsArrayToString(items):
        itemS = "\"items\": [\n"
        for i in range (0,len(items)-1):
            itemS = itemS + "   {\n   \"line_num\": \"{items[i].lineNum}\",\n      "
            itemS = itemS + "\"count\": \"{items[i].count}\",\n      "
            itemS = itemS + "\"item\": {\n        \"upc\": \"{items[i].upc}\"\n      }\n    }"
            if(i<len(items)-1):
                itemS = itemS + ",\n"
            else:
                itemS = itemS + "\n"
        itemS = itemS + "]"
        return itemS
            
    def makeOrder(user_id, orderID, serviceOptionHoldID, initTipCents, address, items):
        conn = http.client.HTTPSConnection("connect.instacart.com")
        itemString = self.itemsArrayToString(items)
        
        payload = "{\n  \"order_id\": \"{orderID}\",\n  \"service_option_hold_id\": {serviceOptionHoldID},\n  \"initial_tip_cents\": {initTipCents},\n   \"birthday\": \"string\",\n  },\n  \"address\": {\n    \"address_line_1\": \"{address[0]}\",\n   \"postal_code\": \"{address[1]}\"\n  },\n  {itemString}\n}"

        headers = {
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Authorization': "Bearer <token>"
            }

        conn.request("POST", "/v2/fulfillment/users/{user_id}/orders/delivery", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        
        return data

    def findStoresPickup(postalCode):
        conn = http.client.HTTPSConnection("connect.instacart.com")
        
        payload = "{\n  \"find_by\": {\n    \"postal_code\": \"" + postalCode + "\"\n  }\n}"
        #Might need this later: #\n    \"address_line_1\": \"" + addressLine1 + "\",

        headers = {
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Authorization': "Bearer <token>"
            }

        conn.request("POST", "/v2/fulfillment/stores/delivery", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        
        return data
    