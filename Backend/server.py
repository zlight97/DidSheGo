from flask import Flask
from flask import request
from flask_cors import CORS
import json

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
            token = "TEST TOKEN"
    response = {"success":success,"token":token}
    return json.dumps(response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)