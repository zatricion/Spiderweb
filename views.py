"""
views imports app, auth, and models, but none of these import views
"""
import demjson
import re

from app import app
from models import User
from forms import RegisterForm

from flask import current_app, session, flash, url_for
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from models import Connection

from flask.ext.security import current_user, login_required, login_user
from forms import SearchForm

# Set up Connection table
@app.before_first_request
def initialize():
  Connection.create_table(fail_silently=True)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login/google')
def login():
    return render_template('profile.html')

@app.route("/profile", methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')

@app.route("/path/<path:word>", methods=['GET'])
def bubbles(word):
    word = re.sub(r"https?:", '', word)
    dists = weighted_node_distances(word)
    node_list = []
    for url in dists:
        if url and 'localhost' not in url:
            node_list.append({'name': url, 'value': 1.0 / dists[url]})
    if node_list:
      return render_template('bubbles.html', node_list=demjson.encode(node_list))
    else:
      return ("Sorry, but no Spiderweb has been created for this URL. "
              + "Pathmark it and check again :)")

@app.route("/test", methods=['POST'])
def test():
    req = request.form
    word = req.get('word', None)
    return demjson.encode(weighted_node_distances(word))

@app.route("/add_mark/<project>", methods=['POST'])
def serve(project):
    link_dict = demjson.decode(request.stream.read())
    for to_url in link_dict:
        from_url = link_dict[to_url][0]['in_node']
        try:
            r = Connection.get(Connection.from_url == from_url, Connection.to_url == to_url, Connection.project == project)
            r.count += 1
        except Connection.DoesNotExist:
            r = Connection(from_url = from_url, to_url = to_url, project = project, count = 1)
            r.save()
            resp = Response(status=200, mimetype='application/json')
    return resp

# Helper Functions

# Go through the database and assemble a list of urls
# rank them by weighted distance from search url
def weighted_node_distances(rootNode):
    rNode = Node(rootNode, 0)
    distances = dict(get_distances(rNode, wDist=0, seen=[]))
    return distances

# wDist is the weighted distance (accumulates edge weights)
def get_distances(node, wDist, seen):
    wDist += node.weight
    for child in get_children(node, seen):
        for each in get_distances(child, wDist, seen):
            yield each
        yield child.url, wDist + child.weight


# get the children of a node from its url (don't include already seen db entries)
def get_children(node, seen):
      url = node.url
                     
      # Database layout is:
      # id | from_url | to_url | count | uuid
      
      # Populate children list
      # Get children from 'incoming' links
      incoming = Connection.select().where(Connection.to_url == url)
      left_children = [Node(n.from_url, n.count) for n in incoming if n.id not in seen]

      # Add seen ids to list
      seen.extend(n.id for n in incoming if n.id not in seen)
      
      # Get children from 'outgoing' links
      outgoing = Connection.select().where(Connection.from_url == url)
      right_children = [Node(n.to_url, n.count) for n in outgoing if n.id not in seen]
      
      # Add seen ids to list
      seen.extend(n.id for n in outgoing if n.id not in seen)

      children = left_children + right_children
      return children
 
# A node has a url and a weight
class Node:
    def __init__(self, url, count):
        self.url = url
        self.weight = (1.0 / count) if count != 0 else count
