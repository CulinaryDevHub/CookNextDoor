from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route("/")
def welcome():
    return 'Hello World'



from controller import * 