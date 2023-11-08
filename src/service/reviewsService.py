import uuid

from flask import request, jsonify, make_response

from src.app import businesses


class reviewService:

    def fetch_all_reviews(id):
        return make_response(jsonify(businesses[id]["reviews"]), 200)

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

    def fetch_one_review(b_id, r_id):
        if b_id in businesses:
            if r_id in businesses[b_id]["reviews"]:
                return make_response(jsonify(businesses[b_id]["reviews"][r_id]), 200)
            else:
                return make_response(jsonify({"error": "Invalid review ID"}), 404)
        else:
            return make_response(jsonify({"error": "Invalid business ID"}), 404)

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

    def delete_review(b_id, r_id):
        if b_id in businesses:
            if r_id in businesses[b_id]["reviews"]:
                del businesses[b_id]["reviews"][r_id]
                return make_response(jsonify({}), 204)
            else:
                return make_response(jsonify({"error": "Invalid review ID"}), 404)
        else:
            return make_response(jsonify({"error": "Invalid business ID"}), 404)
