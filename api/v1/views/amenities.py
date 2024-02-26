#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort
from flask import request


@app_views.route("/amenities/", strict_slashes=False,
                 methods=['GET'])
def amenities():
    """the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """Get a specific Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Get a specific Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route("/amenities/", strict_slashes=False,
                 methods=['POST'])
def post_amenity():
    """Post a specific Amenity object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity_name = data['name']
    new_amenity = Amenity(name=amenity_name)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Update a specific Amenity object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
