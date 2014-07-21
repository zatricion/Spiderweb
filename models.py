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

class Role(db.Model, RoleMixin):
    name = TextField(unique=True)
    description = TextField(null=True)

class User(db.Model, UserMixin):
    email = TextField(null=True)
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
    user = ForeignKeyField(User, related_name = 'user_id')
    provider_id = CharField(null=True)
    provider_user_id = CharField(null=True)
    access_token = CharField(null=True)
    secret = CharField(null=True)
    display_name = CharField(null=True) 
    profile_url = CharField(null=True)
    image_url = CharField(null=True)
    rank = IntegerField(null=True)

app.security = Security(app, PeeweeUserDatastore(db, User, Role, UserRoles))
app.social = Social(app, PeeweeConnectionDatastore(db, Google))
