import mysql.connector as mysql
import os
 
# Set values of local variables to the db credentials from env variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# Try to create table. Print error if it doesn't work.
try:
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS user_data (
			user_id          	integer  AUTO_INCREMENT PRIMARY KEY,
			first_name  	VARCHAR(50),
			last_name		VARCHAR(50),
			email			VARCHAR(50),
			address 		VARCHAR(50),
			city			VARCHAR(50),
			state			VARCHAR(2),
			zipcode			VARCHAR(10),
			order_day		INT,
			order_method	INT,
			cart_table		VARCHAR(50),
			created_at		TIMESTAMP
		);
	""")
	print ('Created Table user_data')
except RuntimeError as err:
	print("runtime error: {0}".format(err))

# Try to create table. Print error if it doesn't work.
try:
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS pairing_requests (
			request_id integer AUTO_INCREMENT PRIMARY KEY,
			user_id integer,
			IP VARCHAR(30),
			created_at		TIMESTAMP
		);
	""")
	print ('Created Table pairing_requests')
except RuntimeError as err:
	print("runtime error: {0}".format(err))

db.commit()