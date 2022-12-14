#!/usr/bin/python3
'''rest api entry module'''

from models import storage
from api.v1.views import app_views, api
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from os import environ
# from flask_restplus import Api
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["JWT_SECRET_KEY"] = "super-secret" 
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
jwt = JWTManager(app)

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, debug=True, threaded=True)
