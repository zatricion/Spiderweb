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
    link_dict = request.form
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

@app.route("/clouds.json")
def clouds():
    data = Connection.get(Connection.from_url == "hi")
    resp = Response(demjson.encode([data.to_url, data.count]), status=200, mimetype='application/json')
    return resp
