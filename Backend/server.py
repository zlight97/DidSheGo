from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/submitlogin", methods = ['POST'])
def increment():
    if request.method == 'POST':
        data = request.form # this should be a dict of params
    else:
        pass #This is an error case

if __name__ == "__main__":
    app.run(port=5000, debug=True)