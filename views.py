"""
views imports app, auth, and models, but none of these import views
"""

from app import app

from flask import Flask
from flask import Response
from flask import json
from flask import request

from models import Connection


@app.route("/", methods=['GET'])
def home():
    return "hello, world"

@app.route("/", methods=['POST'])
def serve():
    req = request.form
    rtype = req.get('type', None)
    if rtype == "search":
        return "cool search, bro"
    elif rtype == "new_pathmark":
        return "added some info"
    else:
      return Response("hi", status=200, mimetype='application/json')

@app.route("/clouds.json")
def clouds():
    data = Connection.get(Connection.from_url == "hi")
    resp = Response(json.dumps([data.to_url, data.count]), status=200, mimetype='application/json')
    return resp
