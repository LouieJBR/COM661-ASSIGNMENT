import datetime
from functools import wraps

import bcrypt
import jwt
from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient

import businessService
import reviewService

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB  # select the database
businesses = db.biz  # select the collection
staff = db.staff
blacklist = db.blacklist

app.config['SECRET_KEY'] = 'mysecret'

BASE_URL = '/api/v1.0'


def pagination(list):
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    list_response = [{k: v} for k, v in list.items()]
    data_to_return = list_response[page_start: page_start + page_size]
    return make_response(jsonify(data_to_return), 200)


def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify( \
                {'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, \
                              app.config['SECRET_KEY'])
        except:
            return jsonify( \
                {'message': 'Token is invalid'}), 401

        bl_token = blacklist.find_one({"token": token})
        if bl_token is not None:
            return make_response(jsonify( \
                {'message': \
                     'Token has been cancelled. This session was ended.'}), 401)
        return func(*args, **kwargs)

    return jwt_required_wrapper


def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers['x-access-token']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        if data['admin']:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({'message': 'Administrator access is required for this operation'}), 401)

    return admin_required_wrapper


@app.route(BASE_URL + '/login', methods=['GET'])
def login():
    auth = request.authorization

    if auth:
        user = staff.find_one({'username': auth.username})
        if user is not None:
            if bcrypt.checkpw(bytes(auth.password, 'UTF-8'), \
                              user["password"]):
                token = jwt.encode( \
                    {'user': auth.username, \
                     'admin': user['admin'],
                     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, \
                    app.config['SECRET_KEY'])
                return make_response(jsonify( \
                    {'token': token.decode('UTF-8')}), 200)
            else:
                return make_response(jsonify( \
                    {'message': 'Incorrect Password'}), 401)
        else:
            return make_response(jsonify( \
                {'message': 'Incorrect Username'}), 401)

    return make_response(jsonify( \
        {'message': 'Authentication required'}), 401)


@app.route(BASE_URL + '/logout', methods=["GET"])
@jwt_required
def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token": token})
    return make_response(jsonify( \
        {'message': 'Logout successful'}), 200)


@app.route(BASE_URL + "/businesses", methods=["GET"])
def return_all_businesses():
    return businessService.return_all_businesses()


@app.route(BASE_URL + "/businesses/<string:id>", methods=["GET"])
def return_one_business(id):
    return businessService.return_one_business(id)


@app.route(BASE_URL + "/businesses", methods=["POST"])
@jwt_required
def add_new_business():
    return businessService.add_new_business()


@app.route(BASE_URL + "/businesses/<string:id>", methods=["PUT"])
@jwt_required
def edit_business(id):
    return businessService.edit_business(id)


@app.route(BASE_URL + "/businesses/<string:id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_business(id):
    return businessService.delete_business(id)


@app.route(BASE_URL + "/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    return reviewService.fetch_all_reviews(id)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews", methods=["POST"])
def add_new_review(b_id):
    return reviewService.add_new_review(b_id)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    return reviewService.fetch_one_review(b_id, r_id)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["PUT"])
@jwt_required
def edit_review(b_id, r_id):
    return reviewService.edit_review(b_id, r_id)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_review(b_id, r_id):
    return reviewService.delete_review(b_id, r_id)


if __name__ == "__main__":
    businessService.businesses = businesses
    reviewService.businesses = businesses
    app.run(debug=True)
