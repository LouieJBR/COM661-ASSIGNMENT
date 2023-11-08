import random
import uuid

from flask import Flask, request, jsonify, make_response
import businessService
import reviewService
import jwt
import datetime
from functools import wraps

from utils import Utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

BASE_URL = '/api/v1.0'


def generate_dummy_data():
    towns = ['Coleraine', 'Banbridge', 'Belfast',
             'Lisburn', 'Ballymena', 'Derry', 'Newry',
             'Enniskillen', 'Omagh', 'Ballymena']
    business_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i)
        town = towns[random.randint(0, len(towns) - 1)]
        rating = random.randint(1, 5)
        business_dict[id] = {
            "name": name, "town": town,
            "rating": rating, "reviews": {}
        }
    return business_dict


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
        return func(*args, **kwargs)

    return jwt_required_wrapper


@app.route(BASE_URL + '/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode( \
            {'user': auth.username, \
             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, \
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401,
                         {'WWW-Authenticate': 'Basic realm = "Login required'})


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
def delete_review(b_id, r_id):
    return reviewService.delete_review(b_id, r_id)


if __name__ == "__main__":
    data = Utils.generate_dummy_data()
    businessService.businesses = data
    reviewService.businesses = data
    app.run(debug=True)
