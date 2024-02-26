#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models.state import State, City
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort
from flask import request


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def cities(state_id):
    """the list of all City objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City).values()
    state_cities = [city.to_dict() for city in cities if
                    city.state_id == state_id]
    return jsonify(state_cities), 200


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['GET'])
def get_city(city_id):
    """Get a specific City object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Get a specific State object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """Post a specific State object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    city_name = data['name']
    new_city = City(name=city_name, state_id=state_id)

    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("cities/<city_id>", strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """Update a specific State object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    # Get State with corresponding id
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
