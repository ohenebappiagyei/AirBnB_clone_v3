#!/usr/bin/python3
"""The api's application module"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(error):
    """Method to handle teardown context"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles 404 not found errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
