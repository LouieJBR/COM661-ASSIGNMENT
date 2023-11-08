from flask import Flask, request, jsonify, make_response
import uuid, random

BASE_URL = '/api/v1.0/'

businesses = {}


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


app = Flask(__name__)


@app.route(BASE_URL + "/businesses", methods=["GET"])
def return_all_businesses():
    all_businesses = pagination(businesses)
    return make_response(all_businesses, 200)


@app.route(BASE_URL + "/businesses/<string:id>", methods=["GET"])
def return_one_business(id):
    if id in businesses:
        return make_response(jsonify(businesses[id]), 200)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)


@app.route(BASE_URL + "/businesses", methods=["POST"])
def add_new_business():
    if "name" in request.form and request.form["name"] != "":
        if "town" in request.form and request.form["town"] != "":
            if "rating" in request.form and request.form["rating"] != "":
                next_id = str(uuid.uuid1())
                new_business = {"name": request.form["name"],
                                "town": request.form["town"],
                                "rating": request.form["rating"],
                                "reviews": []
                                }
                businesses[next_id] = new_business
                return make_response(jsonify({next_id: new_business}), 201)
            else:
                return make_response(jsonify({"error": "Missing rating data"}), 404)
        else:
                return make_response(jsonify({"error": "Missing town data"}), 404)
    else:
        return make_response(jsonify({"error": "Missing name data"}), 404)


@app.route(BASE_URL + "/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if id not in businesses:
        return make_response(jsonify({"error": "Invalid Business ID"}), 404)
    else:
        if "name" and "town" and "rating" in request.form:
            businesses[id]["name"] = request.form["name"]
            businesses[id]["town"] = request.form["town"]
            businesses[id]["rating"] = request.form["rating"]
            return make_response(jsonify({id: businesses[id]}), 200)
        else:
            return make_response(jsonify({"error": "Missing form data"}), 404)


@app.route(BASE_URL + "/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    if id in businesses:
        del businesses[id]
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)


@app.route(BASE_URL + "/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    return make_response(jsonify(businesses[id]["reviews"]), 200)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews", methods=["POST"])
def add_new_review(b_id):
    if b_id in businesses:
        next_id = str(uuid.uuid1())
        new_review = {
            "username": request.form["username"],
            "comment": request.form["comment"],
            "stars": request.form["stars"]
        }
        businesses[b_id]["reviews"][next_id] = new_review
        return make_response(jsonify({next_id: new_review}), 201)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    if b_id in businesses:
        if r_id in businesses[b_id]["reviews"]:
            return make_response(jsonify(businesses[b_id]["reviews"][r_id]), 200)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["PUT"])
def edit_review(b_id, r_id):
    if b_id in businesses:
        if r_id in businesses[b_id]["reviews"]:
            businesses[b_id]["reviews"][r_id]["username"] = request.form["username"]
            businesses[b_id]["reviews"][r_id]["comment"] = request.form["comment"]
            businesses[b_id]["reviews"][r_id]["stars"] = request.form["stars"]

            return make_response(jsonify(businesses[b_id]["reviews"][r_id]), 200)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)


@app.route(BASE_URL + "/businesses/<string:b_id>/reviews/<string:r_id>", methods=["DELETE"])
def delete_review(b_id, r_id):
    if b_id in businesses:
        if r_id in businesses[b_id]["reviews"]:
            del businesses[b_id]["reviews"][r_id]
            return make_response(jsonify({}), 204)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)

def pagination(list):
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    list_response = [{k:v} for k, v in list.items()]
    data_to_return = list_response[page_start: page_start + page_size]
    return make_response(jsonify(data_to_return), 200)


if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(debug=True)
