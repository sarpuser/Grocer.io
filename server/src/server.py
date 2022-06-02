from wsgiref.simple_server import make_server
from numpy import record
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import FileResponse

import mysql.connector as mysql
import os

''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']


''' Normal Route for an HTML Page '''
def get_home(req):
	return FileResponse('./templates/index.html')

def new_user_page(req):
	return FileResponse('./templates/newuser.html')

def create_user(req):
	# Get user information
	first_name = req.matchdict['fname']
	last_name = req.matchdict['lname']
	email = req.matchdict['email']
	address = req.matchdict['address']
	city = req.matchdict['city']
	state = req.matchdict['state']
	zipcode = req.matchdict['zip']
	order_day = int(req.matchdict['day'])
	order_method = int(req.matchdict['method'])

	# Connect to the database
	db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor = db.cursor()

	query = "SELECT * FROM user_data WHERE email=%s"
	cursor.execute(query, [email])
	record = cursor.fetchone()
	if (record is not None):
		return {'create_user_success': -1, 'email': ''}

	try:
		# Create user entry
		query = "INSERT INTO user_data (first_name, last_name, email, address, city, state, zipcode, order_day, order_method) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (first_name, last_name, email, address, city, state, zipcode, order_day, order_method)
		cursor.execute(query, values)
		db.commit()
	except:
		return {'create_user_success': 0, 'email': ''}

	# Get user id to create cart table
	query = "SELECT user_id FROM user_data WHERE email = %s"
	cursor.execute(query, [email])
	user_id = cursor.fetchone()[0]

	# # Create cart table name and add to user entry
	# cart_table_name = "user_" + str(user_id) + "_cart"
	# query = "UPDATE user_data SET cart_table = %s WHERE user_id = %s"
	# cursor.execute(query, [cart_table_name, user_id])
	# db.commit()

	# # Create the user's cart. All user carts will be called user_{user_id}_cart
	# query = """
	# 	CREATE TABLE IF NOT EXISTS %s (
	# 		barcode INT PRIMARY KEY,
	# 		item_name VARCHAR(100),
	# 		quantity INT,
	# 		updated TIMESTAMP
	# 	)
	# """
	# cursor.execute(query, [cart_table_name])
	# db.commit()
	# db.close()

	return {'create_user_success': 1, 'email': email}

def user_home_page(req):
	email = req.matchdict['email']

	# Connect to the database
	db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor = db.cursor()

	query = "SELECT first_name, last_name, email, address, city, state, zipcode, order_day, order_method FROM user_data WHERE email=%s"
	cursor.execute(query, [email])
	record = cursor.fetchone()		

	if (record[8] == 1):
		order_method = "Delivery"
	elif (record[8] == 2):
		order_method = "Pickup"

	if (record[7] == 0):
		order_day = "Monday"
	elif (record[7] == 1):
		order_day = "Tuesday"
	elif (record[7] == 2):
		order_day = "Wednesday"
	elif (record[7] == 3):
		order_day = "Thursday"
	elif (record[7] == 4):
		order_day = "Friday"
	elif (record[7] == 5):
		order_day = "Saturday"
	elif (record[7] == 6):
		order_day = "Sunday"

	# Create JSON for passing to the jinja templating engine
	user_data = {
		'fname': record[0],
		'lname': record[1],
		'email': record[2],
		'address': record[3],
		'city': record[4],
		'state': record[5],
		'zipcode': record[6],
		'order_day': order_day,
		'order_method': order_method,
	}

	return render_to_response('./templates/user_home.html', user_data, request=req)

def get_cart(req):
	email = req.matchdict['email']

	# Connect to the database
	db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor = db.cursor()

	# Get user id to get cart table
	query = "SELECT user_id, first_name FROM user_data WHERE email = %s"
	cursor.execute(query, [email])
	user_info = cursor.fetchone()[0]
	user_id = user_info[0]
	first_name = user_info[1]

	cart_table_name = "user_" + str(user_id) + "_cart"

	query = "SELECT barcode, item_name, quantity FROM %s"
	cursor.execute(query, [cart_table_name])
	cart_items = cursor.fetchall()
	response = {'cart_items': cart_items, 'fname': first_name}

	return render_to_response('./templates/cart.html', response, request=req)

def add_to_cart(req):
	barcode = req.matchdict['barcode']
	email = req.matchdict['email']
	item_name = "fake" # FIXME: add barcode lookup API

	# Connect to the DB
	db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
	cursor = db.cursor()

	# Get user id to get cart table
	query = "SELECT user_id FROM user_data WHERE email = %s"
	cursor.execute(query, [ ])
	user_id = cursor.fetchone()[0]
	cart_table_name = "user_" + str(user_id) + "_cart"

	query = "SELECT quantity FROM %s"
	if (cursor.execute(query, [cart_table_name]) > 0):
		quantity  = cursor.fetchone()[0] + 1
		query = "UPDATE %s SET quantity=%d WHERE barcode=%s"
		values = (cart_table_name, quantity, barcode)
		cursor.execute(query, values)

	else:
		query = "INSERT INTO %s (barcode, item_name, quantity) VALUES (%s, %s, 0)"
		values  = (cart_table_name, barcode, item_name)
		cursor.execute(query, values)
	db.commit()

	return {'added_to_cart': 1}

def request_user_id(req):
	IP = req.remote_addr

	# Connect to the DB
	db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
	cursor = db.cursor()

	# return the user_id that matches the IP from the rpi
	query = "SELECT user_id FROM pairing_requests WHERE IP = %s"
	cursor.execute(query, [IP])
	user_id = cursor.fetchone()[0]

	#now delete the the IP from pairing_requests now that we have paired
	query = "DELETE FROM pairing_requests WHERE IP = %s"
	cursor.execute(query, [IP])

	return {"user_id" : user_id}

def pair(req):
	email = req.matchdict['email']
	IP = req.remote_addr

	# Connect to the database
	db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor = db.cursor()

	query = 'SELECT user_id FROM user_data WHERE email=%s'
	cursor.execute(query, [email])
	user_id = cursor.fetchone()[0]

	query = 'INSERT INTO pairing_requests (user_id, IP) VALUES (%s, %s)'
	cursor.execute(query, [user_id, IP])

	return {}

def get_pairing_status(req):
	IP = req.remote_addr

	# Connect to the database
	db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor = db.cursor()

	query = 'SELECT * FROM pairing_requests WHERE IP=%s'
	cursor.execute(query, [IP])
	record = cursor.fetchall()

	if (record is None):
		return {'pairing_status': 1}
	else:
		return {'pairing_status': 0}

def check_user(req):
	email = req.matchdict['email']

	# Connect to the database
	db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor = db.cursor()

	query = 'SELECT * FROM user_data WHERE email=%s'
	cursor.execute(query, [email])
	record = cursor.fetchone()

	if (record is None):
		return {'user_found': 0}
	else: 
		return {'user_found': 1}

''' Route Configurations '''
if __name__ == '__main__':
	with Configurator() as config:

		# to use Jinja2 to render the template!
		config.include('pyramid_jinja2')
		config.add_jinja2_renderer('.html')

		# Home route
		config.add_route('get_home', '/')
		config.add_view(get_home, route_name='get_home')

		# add new user data route
		config.add_route('create_user', '/adduser/{fname}/{lname}/{email}/{address}/{city}/{state}/{zip}/{day}/{method}')
		config.add_view(create_user, route_name='create_user', renderer='json')

		# User home route
		config.add_route('get_user', '/user/{email}')
		config.add_view(user_home_page, route_name='get_user')

		# New user form route
		config.add_route('new_user', '/newuser')
		config.add_view(new_user_page, route_name='new_user')

		# User cart route
		config.add_route('get_cart', '/cart/{email}')
		config.add_view(get_cart, route_name='get_cart')

		# Add to cart route
		config.add_route('add_to_cart', '/additem/{email}/{barcode}')
		config.add_view(add_to_cart, route_name='add_to_cart')

		# request user_id route
		config.add_route('request_user_id', '/request_user_id/')
		config.add_view(request_user_id, route_name='request_user_id', renderer='json')

		# find user for login route
		config.add_route('check_user', '/find/{email}')
		config.add_view(check_user, route_name='check_user', renderer='json')

		# pairing request route
		config.add_route('pairing', '/pair/{email}')
		config.add_view(pair, route_name='pairing', renderer='json')

		# pairing status route
		config.add_route('pairing_status', '/get_pairing_status')
		config.add_view(get_pairing_status, route_name='pairing_status', renderer='json')

		# For our static assets!
		config.add_static_view(name='/', path='./public', cache_max_age=3600)

		app = config.make_wsgi_app()

	server = make_server('0.0.0.0', 80, app)
	print('Web server started on: http://0.0.0.0 or http://127.0.0.1 or http://localhost')
	server.serve_forever()
