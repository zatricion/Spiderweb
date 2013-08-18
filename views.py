"""
views imports app, auth, and models, but none of these import views
"""
import demjson

from app import app

from flask import Flask
from flask import Response
from flask import request
import json
from models import Connection


@app.route("/", methods=['GET'])
def home():
    return "hello, world"

@app.route("/add_mark", methods=['POST'])
def serve():

    resp = Response(json.dumps(request.form), status=200, mimetype='application/json')
    return resp

@app.route("/clouds.json")
def clouds():
    data = Connection.get(Connection.from_url == "hi")
    resp = Response(demjson.encode([data.to_url, data.count]), status=200, mimetype='application/json')
    return resp
