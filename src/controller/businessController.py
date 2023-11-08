from ..service.businessService import businessService
from __main__ import app
from flask import Blueprint

business_controller_blueprint = Blueprint('business_controller_blueprint', __name__, url_prefix='api/')

BASE_URL = '/api/v1.0/'


@business_controller_blueprint.route(BASE_URL + "/businesses", methods=["GET"])
def return_all_businesses():
    businessService.return_all_businesses()


@app.route(BASE_URL + "/businesses/<string:id>", methods=["GET"])
def return_one_business(id):
    businessService.return_one_business(id)


@app.route(BASE_URL + "/businesses", methods=["POST"])
def add_new_business():
    businessService.add_new_business()


@app.route(BASE_URL + "/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    businessService.edit_business(id)


@app.route(BASE_URL + "/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    businessService.delete_business(id)
