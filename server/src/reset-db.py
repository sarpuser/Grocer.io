import mysql.connector as mysql
import os
 
# Set values of local variables to the db credentials from env variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

# Try to create table. Print error if it doesn't work.
try:
	cursor.execute('DROP DATABASE IF EXISTS GrocerIO;')
	cursor.execute('CREATE DATABASE GrocerIO;')
	print ('Re-created blank database GrocerIO')
except RuntimeError as err:
	print("runtime error: {0}".format(err))

db.commit()