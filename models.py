"""
models imports app, but app does not import models so we haven't created
any loops.
"""

from peewee import *
from flask.ext.security import Security, PeeweeUserDatastore, UserMixin, RoleMixin
from flask.ext.social import Social
from flask.ext.social.datastore import PeeweeConnectionDatastore
from app import db
from app import app

class Connection(db.Model):
    from_url = CharField()  
    to_url = CharField()
    count = IntegerField()
    project = CharField()


db = Database(app)

class Role(db.Model, RoleMixin):
    name = TextField(unique=True)
    description = TextField(null=True)

class User(db.Model, UserMixin):
    email = TextField()
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)

class UserRoles(db.Model):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)

class Google(db.Model):
    user_id = ForeignKeyField(User, related_name = 'user_id')
    provider_id = CharField()
    provider_user_id = CharField()
    access_token = CharField()
    secret = CharField()
    display_name = CharField() 
    profile_url = CharField()
    image_url = CharField()
    rank = IntegerField()

security = Security(app, PeeweeUserDatastore(db, User, Role, UserRoles))
social = Social(app, PeeweeConnectionDatastore(db, Google))
