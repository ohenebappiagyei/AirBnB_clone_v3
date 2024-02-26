#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort
from flask import request


@app_views.route("/users", strict_slashes=False, methods=['GET'])
def users():
    """the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Get a specific User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Get a specific User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_user():
    """Post a specific User object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user_name = data['name']
    email = data['email']
    password = data['password']
    new_user = User(name=user_name, email=email, password=password)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Update a specific User object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
