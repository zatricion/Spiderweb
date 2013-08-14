from flask import Flask

app = Flask(__name__)

# flask-peewee database, but could be SQLAlchemy instead.
from flask_peewee.db import Database

app.config.from_object('config.Configuration')

# instantiate the db wrapper
db = Database(app)
