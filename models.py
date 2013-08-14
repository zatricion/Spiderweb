"""
models imports app, but app does not import models so we haven't created
any loops.
"""

from peewee import *

from app import db

class Connections(db.Model):
    search_url = CharField()  
    find_url = CharField()
