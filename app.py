from flask import Flask
from flask import Blueprint
import os

app = Flask(__name__)

# add Foundation static files
bower = Blueprint('bower', __name__, static_folder='bower_components')
app.register_blueprint(bower)

js = Blueprint('js', __name__, static_folder='js')
app.register_blueprint(js)

style = Blueprint('style', __name__, static_folder='stylesheets')
app.register_blueprint(style)

# flask-peewee database, but could be SQLAlchemy instead.
from flask_peewee.db import Database

app.config.from_object('config.Configuration')

# Add secret key
app.secret_key = os.urandom(24)

# instantiate the db wrapper
db = Database(app)
