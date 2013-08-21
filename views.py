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
    
    # wDist is the weighted distance (accumulates edge weights)
    def distance_dict(node, wDist=None):
        wDist = 0 if wDist == None else wDist
        for child in get_children(node):
            wDist += (1.0 / child.count)
            if !child.is_leaf:
                for each in distance_dict(child, wDist):
                    yield each
        yield child.url, wDist
  
def weighted_node_distances(rootNode):
    distances = dict(distance_dict(rootNode))
    return demjson.encode(distances)

# node Class
class Node:
    def __init__(self, url, count):
        self.url = url
        self.count = count
            
        def is_leaf(self):
            return bool(get_children(self))

# get the children of a node from its url
def get_children(node):
      url = node.url
                  
      # Populate children list
      children = from_db('left', url).extend(from_db('right', url))
      return children
      
      
def from_db(side, url)):
      children = []
      right = True if side == 'right' else False
      thisUrl = Connection.from_url if right else Connection.to_url
      while True:
            try:
                  nextCon = Connection.get(thisUrl == url)
                  nextUrl = nextCon.to_url if right else nextCon.from_url
                  if nextUrl in nodes:
                        break
                  url = nextUrl
                  children.append(Node(url, nextCon.count))
                  
            except Connection.DoesNotExist:
                  break
      return children
