from flask import Flask
from flask_bcrypt import Bcrypt
from routes import vendor_routes, customer_routes
from flask_cors import CORS

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)

@app.route("/")
def welcome():
    return 'Hello World'

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200
    
# Register API routes
app.register_blueprint(vendor_routes, url_prefix='/api/vendor')
app.register_blueprint(customer_routes, url_prefix='/api/customer')

if __name__ == "__main__":
    app.run(debug=True)


from controller import * 