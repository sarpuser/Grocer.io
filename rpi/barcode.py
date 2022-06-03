import sys
import requests
import json

api_key = "" #https://upcdatabase.org/
user_id_file_path = "user_id.txt"
url = "http://164.92.97.79/additem/"

def barcode_reader():
    """Barcode code obtained from 'brechmos' 
    https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100"""
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

    fp = open('/dev/hidraw0', 'rb')

    ss = ""

    done = False

    while not done:

        ## Get the character from the HID
        buffer = fp.read(3)
        for c in buffer:
            if(int(c) > 0):

                if(int(c) == 40):
                    done = True
                else:
                    ss += hid[int(c)]
    return ss


#Make restful request to server
def restful_request(upc_code):
    USER_ID = read_USER_ID()
    r = requests.get(url + str(USER_ID) + "/" + str(upc_code)) #http://164.92.97.79/additem/USER_ID/BARCODE

def read_USER_ID():
    f = open(user_id_file_path, "r")
    line = f.readline()
    split_line = line.split(":")
    USER_ID = split_line[1].strip()
    f.close()

    return USER_ID

"""
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

UPC lookup disabled because instacart API requires input UPC code, so all we need is the barcode scanner output

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

# def UPC_lookup(api_key,upc):
#     '''V3 API'''

#     url = "https://api.upcdatabase.org/product/%s/%s" % (upc, api_key)

#     headers = {
#         'cache-control': "no-cache",
#     }

#     response = requests.request("GET", url, headers=headers)

#     print("-----" * 5)
#     print(upc)
#     print(json.dumps(response.json(), indent=2))
#     print("-----" * 5 + "\n")


if __name__ == '__main__':
    try:
        while True:
            barcode = barcode_reader()
            print(barcode)
            restful_request(barcode)
    except KeyboardInterrupt:
        pass