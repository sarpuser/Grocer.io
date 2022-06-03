import os
import requests

'''Get API Key'''
api_key = os.environ['BARCODE_API_KEY']

def lookup_barcode(barcode):
	url = 'https://api.barcodelookup.com/v3/products?barcode=' + str(barcode) + '&formatted=y&key=' + api_key
	response = requests.get(url)
	print (response)


if __name__ == "__main__":
	lookup_barcode(738435248451)