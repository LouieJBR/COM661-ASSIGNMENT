from ..service.reviewsService import reviewService
from __main__ import app
from flask import Blueprint

review_controller_blueprint = Blueprint('review_controller_blueprint', __name__, url_prefix='api/')

BASE_URL = '/api/v1.0/'


@review_controller_blueprint.route(BASE_URL + "/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    reviewService.fetch_all_reviews(id)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews", methods=["POST"])
def add_new_review(b_id):
    reviewService.add_new_review(b_id)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    reviewService.fetch_one_review(b_id, r_id)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["PUT"])
def edit_review(b_id, r_id):
    reviewService.edit_review(b_id, r_id)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["DELETE"])
def delete_review(b_id, r_id):
    reviewService.delete_review(b_id, r_id)
