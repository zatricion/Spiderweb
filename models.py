"""
models imports app, but app does not import models so we haven't created
any loops.
"""

from peewee import *

from app import db

class Connection(db.Model):
    from_url = CharField()  
    to_url = CharField()
    count = IntegerField()
