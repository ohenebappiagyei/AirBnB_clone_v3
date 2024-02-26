#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort
from flask import request


@app_views.route("/states/", strict_slashes=False,
                 methods=['GET'])
def states():
    """the list of all State objects"""
    statess = storage.all(State).values()
    return jsonify([state.to_dict() for state in statess])


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['GET'])
def get_state(state_id):
    """Get a specific State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Get a specific State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route("/states/", strict_slashes=False,
                 methods=['POST'])
def post_state():
    """Post a specific State object by ID"""
    # Parse JSON data from request body
    data = request.get_json()
    # Check if request body is valid JSON
    if data is None:
        abort(400, 'Not a JSON')
    # Check is 'name' key is in data(JSON data)
    if 'name' not in data:
        abort(400, 'Missing name')
    # Extract state name for data and use
    # in creating new state. This step is not
    # particularly necessary
    state_name = data['name']

    # Create a new State object
    new_state = State(name=state_name)
    # Can be rewritten as
    # new_state = State(name=data['name'])

    storage.new(new_state)  # Save the new State
    storage.save()
    # return new State with 201
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """Update a specific State object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    # Get State with corresponding id
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in data.items():
        # Ignore keys: id, created_at and updated_at
        if key not in ['id', 'created_at', 'updated_at']:
            # Update the State object with
            # all key-value pairs of the dictionary.
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
