import jwt.utils
import time
import math
import requests
import uuid
import http.client


class DoorDash: # API Class for using DoorDash API
    
    def __init__(self, pickupAddress, pickupPhoneNumber, dropoffAddress, dropoffPhoneNumber): # Pass in the REQUIRED parts of request
        self.pickupAddress = pickupAddress
        self.pickupPhoneNumber = pickupPhoneNumber
        self.dropoffAddress = dropoffAddress
        self.dropoffPhoneNumber = dropoffPhoneNumber
    
    access_key = {
    "developer_id": "9e05e3d3-77fb-4316-9e66-1d7bbae90127",
    "key_id": "0e1c10c7-b4f1-4da6-80c0-92eec4aec9ad",
    "signing_secret": "6PzwYTKjYgAam4U98t9RN_U0ZPyuqE1X8EQF-KDaJiY"
    }

    token = jwt.encode(
        {   
            "aud": "doordash",
            "iss": access_key["developer_id"],
            "kid": access_key["key_id"],
            "exp": str(math.floor(time.time() + 60)),
            "iat": str(math.floor(time.time())), 
        },
        jwt.utils.base64url_decode("{signing_secret}"),
        algorithm="HS256",
        headers={"dd-ver": "DD-JWT-V1"})
    
    def createDelivery():
        endpoint = "https://openapi.doordash.com/drive/v2/deliveries/"  # DRIVE API V2
    
        headers = {"Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"}

        delivery_id = str(uuid.uuid4()) # Randomly generated UUID4

        request_body = { # Modify pickup and drop off addresses below
            "external_delivery_id": delivery_id,
            "pickup_address": self.pickupAddress,
            # "pickup_business_name": "not given",
            "pickup_phone_number": self.pickupPhoneNumber,
           # "pickup_instructions": "Enter gate code 1234 on the callbox.",
            "dropoff_address": self.dropoffAddress,
            #"dropoff_business_name": "Wells Fargo SF Downtown",
            "dropoff_phone_number": self.dropoffPhoneNumber
            #"dropoff_instructions": "Enter gate code 1234 on the callbox.",
            #"order_value": 1999
        }
        
        create_delivery = requests.post(endpoint, headers=headers, json=request_body) # Create POST request

        return create_delivery.status_code, create_delivery.text, create_delivery.reason
    
    
    
    
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
    
    def makeOrder(user_id, orderID, serviceOptionHoldID, initTipCents, address, items):
        conn = http.client.HTTPSConnection("connect.instacart.com")

        payload = "{\n  \"order_id\": \"{orderID}\",\n  \"service_option_hold_id\": {serviceOptionHoldID},\n  \"initial_tip_cents\": {initTipCents},\n   \"birthday\": \"string\",\n  },\n  \"address\": {\n    \"address_line_1\": \"{address[0]}\",\n   \"postal_code\": \"{address[1]}\"\n  },\n  \"items\": [\n    {\n      \"line_num\": \"string\",\n      \"count\": 1,\n      \"weight\": 1,\n      \"special_instructions\": \"string\",\n      \"replacement_policy\": \"no_replacements\",\n      \"replacement_items\": [\n        {\n          \"upc\": \"string\"\n        }\n      ],\n      \"item\": {\n        \"upc\": \"string\"\n      }\n    }\n  ]\n}"

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
    
# Mock Door Dash Order for Primos to 
DDObj = DoorDash("7770 Regents Rd #109 San Diego, CA 92122", "+18586380003", "3425 Lebon Dr San Diego, CA 92122", "+19515673759") 

status_code, text, reason = DDObj.createDelivery()

print(status_code)
print(text)
print(reason)