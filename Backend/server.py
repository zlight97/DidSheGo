from flask import Flask
from flask import request
from flask_cors import CORS
import flask
import json
from time import time
import DidSheGo as dsg

app = Flask(__name__)
CORS(app)

def validateToken(token):
    return "test" in token

def getPetData(token):
    data = flask.jsonify(dsg.getPetData(token))
    return data

@app.route("/submitlogin", methods = ['POST'])
def login():
    success = False
    token = ""
    print("/submitlogin received")
    if request.method == 'POST':
        data = request.get_json() # this should be a dict of params
        if "email" in data and "password" in data:
            try:
                token = dsg.login(data["email"], data["password"])
                if token:
                    success = True
            except:
                return flask.jsonify({"success":False})
    return flask.jsonify({"success":success,"token":token})

@app.route("/submitTime", methods = ['POST'])
def submitTime():
    success = False
    token = ""
    if request.method == 'POST':
        data = request.get_json() # this should be a dict of params
        if "auth" in data and "id" in data and "time" in data:
            if validateToken(data["auth"]):
                success = True
                #update with time for pet id, use latest submitted user with id from validation table
                pass
    return flask.jsonify({"success":success,"token":token})

@app.route("/getpets", methods = ['GET'])
def getPets():
    response = flask.jsonify()
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == "GET":
        token = request.headers.get('Access-Token')
        print(token)
        response = getPetData(token)
    print(request)
    return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)