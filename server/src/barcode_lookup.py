import os
import requests

'''Get API Key'''
api_key = os.environ['BARCODE_API_KEY']

def lookup_barcode(barcode):
	url = 'https://api.barcodelookup.com/v3/products?barcode=' + barcode + '&formatted=y&key=' + api_key
	response = requests.get(url)
	response = response.json()['products'][0]
	item_name = (response['title'])
	item_img_src = response['images'][0]
	return item_name, item_img_src


if __name__ == "__main__":
	item_name, img_src = lookup_barcode('738435248451')
	print (item_name, img_src)