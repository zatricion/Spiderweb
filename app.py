from flask import Flask
import os

app = Flask(__name__)

# flask-peewee database, but could be SQLAlchemy instead.
from flask_peewee.db import Database

app.config.from_object('config.Configuration')

# Add secret key
app.secret_key = os.urandom(24)

# instantiate the db wrapper
db = Database(app)
