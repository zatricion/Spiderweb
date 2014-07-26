"""
models imports app, but app does not import models so we haven't created
any loops.
"""

from peewee import *
from app import db
from app import app

class Connection(db.Model):
    from_url = CharField()  
    to_url = CharField()
    count = IntegerField()
    project = CharField()
    email = CharField()

class Tokens(db.Model):
    acct = TextField()  
    refresh_token = TextField()