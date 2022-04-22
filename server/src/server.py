from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

import mysql.connector as mysql
import os

''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']


''' Normal Route for an HTML Page '''
def get_home(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select id, first_name, last_name, email, age from Actors;")
  records = cursor.fetchall()
  db.close()

  return render_to_response('index.html', {"actors":records}, request=req)


''' Collection Route to GET Actors '''
def get_actors(req):
  # Connect to the database and retrieve the actors
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select id, first_name, last_name, email, age from Actors;")
  records = cursor.fetchall()
  db.close()

  # Format the result as key-value pairs
  response = {}
  for index, row in enumerate(records):
    response[index] = {
      "id": row[0],
      "first_name": row[1],
      "last_name": row[2],
      "email": row[3],
      "age": row[4]
    }

  return response


''' Instance Route to GET Actor '''
def get_actor(req):
  # Retrieve the route argument (this is not GET/POST data!)
  the_id = req.matchdict['actor_id']

  # Connect to the database and retrieve the actor
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from Actors where id='%s';" % the_id)
  record = cursor.fetchone()
  db.close()

  if record is None:
    return ""

  # Format the result as key-value pairs
  response = {
    'id':         record[0],
    'first_name': record[1],
    'last_name':  record[2],
    'email':      record[3],
    'age':        record[4],
    'datetime':   record[5].isoformat()
  }

  return response


''' Route Configurations '''
if __name__ == '__main__':
  with Configurator() as config:

    # to use Jinja2 to render the template!
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    # Home route
    config.add_route('get_home', '/')
    config.add_view(get_home, route_name='get_home')

    # RESTful collection route
    config.add_route('get_actors', '/actors')
    config.add_view(get_actors, route_name='get_actors', renderer='json')

    # RESTful instance route
    config.add_route('get_actor', '/actor/{actor_id}')
    config.add_view(get_actor, route_name='get_actor', renderer='json')

    # For our static assets!
    config.add_static_view(name='/', path='./public', cache_max_age=3600)

    app = config.make_wsgi_app()

  server = make_server('0.0.0.0', 80, app)
  print('Web server started on: http://0.0.0.0 or http://127.0.0.1 or http://localhost')
  server.serve_forever()
