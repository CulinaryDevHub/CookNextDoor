from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager 
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)


CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}},  methods=["GET", "POST", "OPTIONS", "DELETE"]) 
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}},  methods=["GET", "POST", "OPTIONS"]) 

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# Pass bcrypt & jwt when importing user_controller
from controller.user_controller import create_user_blueprint
user_bp = create_user_blueprint(bcrypt, jwt)
app.register_blueprint(user_bp)

@app.route("/")
def welcome():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
