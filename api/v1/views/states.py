#!/usr/bin/python3
""" state view """
from flask import jsonify, abort, request
from models import State
from api.v1.views import app_views, storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = [state.to_dict() for state in State.all()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = State.get(state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = State.get(state_id)
    if state is None:
        abort(404)
    state.delete()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = State.get(state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    # Remove keys that should be ignored
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
