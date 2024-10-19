from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
bcrypt = Bcrypt(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}},  methods=["GET", "POST", "OPTIONS"]) 

@app.route("/")
def welcome():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)

from controller import * 