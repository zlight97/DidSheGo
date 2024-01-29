from flask import Flask
from flask import request
from flask_cors import CORS
import flask
import json
from time import time

app = Flask(__name__)
CORS(app)

@app.route("/submitlogin", methods = ['POST'])
def login():
    success = False
    token = ""
    if request.method == 'POST':
        data = request.get_json() # this should be a dict of params
        if "username" in data and "password" in data:
            success = True
            token = "test token"
    return flask.jsonify({"success":success,"token":token})

@app.route("/getpets", methods = ['GET'])
def getPets():
    response = flask.jsonify()
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == "GET":
        data = request.headers.get('Access-Token')
        print(data)
        if 'test' in data:
            response= flask.jsonify({'Gracie':[('pee',1,int(time())),('poop',2,int(time()))]})
    print(request)
    return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)