from flask import current_app
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField

class RegisterForm(Form):
    email = TextField('Email')
    password = PasswordField('Password')
    confirm = PasswordField('Confirm Password')
