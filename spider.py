"""
this is the "secret sauce" -- a single entry-point that resolves the
import dependencies.  If you're using blueprints, you can import your
blueprints here too.

then when you want to run your app, you point to main.py or `main.app`
"""
import os
import binascii
from app import db
from app import app
from models import * 
from views import *

from flask.ext.social import login_failed
from flask.ext.social.utils import get_connection_values_from_oauth_response

@app.before_first_request
def initialize():
  Connection.create_table(fail_silently=True)
  Role.create_table(fail_silently=True)
  User.create_table(fail_silently=True)
  UserRoles.create_table(fail_silently=True)
  Google.create_table(fail_silently=True)


@login_failed.connect_via(app) 
def on_login_failed(sender, provider, oauth_response): 
  connection_values = get_connection_values_from_oauth_response(provider, oauth_response) 
  if not connection_values: 
    raise Exception() # TODO 
  
  ds = current_app.security.datastore 
  user = ds.create_user( 
      nickname = connection_values['display_name'], 
      password = binascii.b2a_hex(os.urandom(16)), 
      google_id = connection_values['provider_user_id']) 
  ds.commit() 
  
  connection_values['user_id'] = user.id 
  connect_handler(connection_values, provider) 
  login_user(user, remember=True) 
  ds.commit() 
  return redirect(url_for('profile'))

if __name__ == "__main__":
    Connection.create_table(fail_silently=True)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, extra_files = ['/Users/mdlauria/HS/Arachnid/spiderweb/templates/'])
