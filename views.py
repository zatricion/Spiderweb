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
    node_list = weighted_node_distances(word)
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
    pass

# wDist is the weighted distance (accumulates edge weights)
def node_distances(node, wDist, seen):
    for child in get_children(node, seen):
        wDist += child.weight
        for each in node_distances(child, wDist, seen):
            yield each
        yield child.url, wDist
  
def weighted_node_distances(rootNode):
    rNode = Node(rootNode, 1)
    distances = dict(node_distances(rNode, wDist=0, seen=[]))
    return demjson.encode(distances)

# get the children of a node from its url (don't include already seen db entries)
def get_children(node, seen):
      url = node.url
                     
      # Database layout is:
      # id | from_url | to_url | count
      
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
        self.weight = (1.0 / count)
