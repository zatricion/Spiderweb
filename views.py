"""
views imports app, auth, and models, but none of these import views
"""
import demjson

from app import app

from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from models import Connection

from forms import SearchForm

# Set up Connection table
@app.before_first_request
def initialize():
  Connection.create_table(fail_silently=True)

@app.route("/", methods=['GET'])
def home():
    return render_template('search.html', form=SearchForm())

@app.route("/", methods=['POST'])
def bubbles():
  req = request.form
  word = req.get('word', None)
  node_list = get_bubbles(word)
  return node_list
  #return render_template('bubbles.html', nodes=node_list)

@app.route("/add_mark", methods=['POST'])
def serve():
    link_dict = demjson.decode(request.stream.read())
    for to_url in link_dict:
        from_url = link_dict[to_url][0]['in_node']
        try:
            r = Connection.get(Connection.from_url == from_url, Connection.to_url == to_url)
            r.count += 1
        except Connection.DoesNotExist:
            r = Connection(from_url = from_url, to_url = to_url, count = 1)
        r.save()
    resp = Response(status=200, mimetype='application/json')
    return resp

# Helper Functions

# Go through the database and assemble a list of urls
# rank them by weighted distance from search url
def get_bubbles(url):
  node_dict = {}

  # Put entries in the table from "right-hand" path
  right_dist = 0
  right_url = url
  while True:
    try:
      right = Connection.get(Connection.from_url == right_url)
      right_dist += (1.0 / right.count)
      right_url = right.to_url
      node_dict[right_url] = right_dist
    except Connection.DoesNotExist:
      break

  # Put entries in the table from "left-hand" path
  left_dist = 0
  left_url = url
  while True:
    try:
      left = Connection.get(Connection.to_url == left_url)
      left_dist += (1.0 / left.count)
      left_url = left.from_url
      node_dict[left_url] = left_dist
    except Connection.DoesNotExist:
      break

  return demjson.encode(node_dict)
