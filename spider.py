import os
import binascii
from app import db
from app import app
from models import * 
from views import *

from flask.ext.social import login_failed
from flask.ext.social.views import connect_handler
from flask.ext.social.utils import get_connection_values_from_oauth_response

@app.before_first_request
def initialize():
  Connection.create_table(fail_silently=True)

if __name__ == "__main__":
    Connection.create_table(fail_silently=True)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, extra_files = ['/Users/mdlauria/HS/Arachnid/spiderweb/templates/'])
