#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort
from flask import request


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """the list of all Review objects"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    reviews = storage.all(Review).values()
    place_reviews = [rev.to_dict() for rev in reviews if
                     rev.place_id == place_id]
    return jsonify(place_reviews)


@app_views.route("reviews/<review_id>", strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Get a specific Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Get a specific Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    """Post a specific Review object by ID"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    review_name = data['name']
    text = data['text']
    new_review = Review(name=review_name, place_id=place_id,
                        user_id=user_id, text=text)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Update a specific Review object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
