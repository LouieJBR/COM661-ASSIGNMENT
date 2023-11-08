import uuid

from flask import request, jsonify, make_response

from ..app import businesses
from ..utils import Utils


class businessService:

    def return_all_businesses(self):
        all_businesses = Utils.pagination(businesses)
        return make_response(all_businesses, 200)

    def return_one_business(id):
        if id in businesses:
            return make_response(jsonify(businesses[id]), 200)
        else:
            return make_response(jsonify({"error": "Invalid business ID"}), 404)

    def add_new_business(self):
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

    def delete_business(id):
        if id in businesses:
            del businesses[id]
            return make_response(jsonify({}), 204)
        else:
            return make_response(jsonify({"error": "Invalid business ID"}), 404)
