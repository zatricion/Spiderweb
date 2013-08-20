from flask.ext.wtf import Form
from wtforms import TextField

class SearchForm(Form):
  word = TextField("Enter a URL: ")

