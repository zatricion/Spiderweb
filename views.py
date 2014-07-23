"""
views imports app, auth, and models, but none of these import views
"""
import demjson
import json
import re
import httplib2
import gdata.contacts.service
import gdata.contacts.client
from apiclient.discovery import build
import random
import string
from oauth_utils import OAuthCred2Token

from app import app

from flask import current_app, session, flash, url_for, make_response
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from models import *

from forms import SearchForm
from forms import RegisterForm
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from simplekv.memory import DictStore
from flask.ext.kvsession import KVSessionExtension

# See the simplekv documentation for details
store = DictStore()

# This will replace the app's session handling
KVSessionExtension(store, app)

# Update client_secrets.json with your Google API project information.
# Do not change this assignment.
CLIENT_ID = json.loads(
    open('client_secrets_heroku.json', 'r').read())['web']['client_id']
SERVICE = build('plus', 'v1')
APPLICATION_NAME = 'Spiderweb'

# Set up Connection table
@app.before_first_request
def initialize():
  Connection.create_table(fail_silently=True)

@app.route('/')
def index():
    # Set the Client ID and Application Name in the HTML while
    # serving it.
    response = make_response(
      render_template('index.html',
                      CLIENT_ID=CLIENT_ID,
                      APPLICATION_NAME=APPLICATION_NAME))
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/connect', methods=['POST'])
def connect():
    """Exchange the one-time authorization code for a token and
    store the token in the session."""
    code = request.data
    
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets_heroku.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # An ID Token is a cryptographically-signed JSON object encoded in base 64.
    # Normally, it is critical that you validate an ID Token before you use it,
    # but since you are communicating directly with Google over an
    # intermediary-free HTTPS channel and using your Client Secret to
    # authenticate yourself to Google, you can be confident that the token you
    # receive really comes from Google and is valid. If your server passes the
    # ID Token to other components of your app, it is extremely important that
    # the other components validate the token before using it.
    gplus_id = credentials.id_token['sub']

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    session['credentials'] = credentials
    session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Successfully connected user.', 200))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/disconnect', methods=['POST'])
def disconnect():
    """Revoke current user's token and reset their session."""
    # Only disconnect a connected user.
    credentials = session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del session['credentials']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
        
@app.route('/people', methods=['GET'])
def people():
    """Get list of people user has shared with this app."""
    credentials = session.get('credentials')
    # Only fetch a list of people for connected users.
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    try:
        client = gdata.contacts.client.ContactsClient(source='Spiderweb')
        client.auth_token = OAuthCred2Token(credentials.access_token)
        query = gdata.contacts.client.ContactsQuery()
        query.max_results = 50000
        feed = client.GetContacts(q=query)
        result = []
        
        # Get all email addresses that exist in the database
        for contact in feed.entry:
            try:
                name = contact.name.full_name.text
            except:
                name = "Unknown"
            for email in contact.email:
                q = Connection.select().where(Connection.email == email.address).limit(1)
                if [ans for ans in q]:
                    result.append((name, email.address))
        
        response = make_response(json.dumps(result), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    except AccessTokenRefreshError:
        response = make_response(json.dumps('Failed to refresh access token.'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/projects/<email>', methods=['GET'])
def show_projects(email):
    q = Connection.select().where(Connection.email == email)
    return render_template('list_projects.html', 
                           projects=list(set(entry.project for entry in q)),
                           email=email)

@app.route("/projects/<email>/<name>", methods=['GET'])
def view_project(email, name):
    q = Connection.select().where(Connection.email == email)\
                           .where(Connection.project == name)
    return render_template('visualize.html', pathmark = [[str(mark.from_url), str(mark.to_url)] for mark in q])

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

@app.route("/add_mark/<email>/<project>", methods=['POST'])
def serve(email, project):
    link_dict = demjson.decode(request.stream.read())
    for to_url in link_dict:
        from_url = link_dict[to_url][0]['in_node']
        try:
            r = Connection.get(Connection.from_url == from_url, 
                               Connection.to_url == to_url, 
                               Connection.project == project,  
                               Connection.email == email)
            r.count += 1
        except Connection.DoesNotExist:
            r = Connection(from_url = from_url, 
                           to_url = to_url, 
                           project = project,
                           email = email, 
                           count = 1)
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
      # id | from_url | to_url | count | project | user_email
      
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
