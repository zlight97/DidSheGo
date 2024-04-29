from flask import Flask
from flask import request
from flask_cors import CORS
import flask
import json
from time import time
import DidSheGo as dsg
import utils

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
            token,_ = dsg.actionMarked(data["auth"],data["id"],utils.epochToDatetime(data['time']))
            if token:
                success = True
    return flask.jsonify({"success":success,"token":token})

@app.route("/logout", methods = ['POST'])
def logout():
    token = ""
    if request.method == 'POST':
        data = request.get_json() # this should be a dict of params
        if "auth" in data:
            return flask.jsonify({'success':dsg.deleteAuth(data["auth"])})
    return flask.jsonify({'success':False})


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

@app.route("/newaction", methods = ['POST'])
def newAction():
    token = ""
    if request.method == 'POST':
        data = request.get_json() # this should be a dict of params
        if "auth" in data and "petid" in data and "action" in data:
            return flask.jsonify({'success':dsg.deleteAuth(data["auth"],data["petid"], data["action"])})
    return flask.jsonify({'success':False})    
    
if __name__ == "__main__":
    app.run(port=5000, debug=True)