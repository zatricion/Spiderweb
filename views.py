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
def node_distances(node, wDist=0):
    for child in get_children(node):
        wDist += child.weight
        if not child.is_leaf:
            for each in node_distances(child, wDist):
                yield each
        yield child.url, wDist
  
def weighted_node_distances(rootNode):
    rNode = Node(rootNode, 0)
    distances = dict(node_distances(rNode))
    return demjson.encode(distances)

# get the children of a node from its url
def get_children(node):
      url = node.url
                     
      # Database layout is:
      # id | from_url | to_url | count
      
      # Populate children list
      # Get children from 'incoming' links
      incoming = Connection.select(Connection.to_url == url)
      left_children = [Node(n.url, n.count) for n in incoming]

      # Get children from 'outgoing' links
      outgoing = Connection.select(Connection.from_url == url)
      right_children = [Node(n.url, n.count) for n in outgoing] 
      
      return left_children + right_children
 
# A node has a url and a weight
class Node:
    def __init__(self, url, count):
        self.url = url
        self.weight = (1.0 / count)
            
        def is_leaf(self):
            return bool(get_children(self))
