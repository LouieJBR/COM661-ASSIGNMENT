from bson import ObjectId
from flask import request, jsonify, make_response

businesses = {}


def return_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    data_to_return = []
    for business in businesses.find() \
            .skip(page_start).limit(page_size):
        business['_id'] = str(business['_id'])
        for review in business['reviews']:
            review['_id'] = str(review['_id'])
        data_to_return.append(business)
    return make_response(data_to_return, 200)


def return_one_business(id):
    business = businesses.find_one({'_id': ObjectId(id)})
    if business is not None:
        business['_id'] = str(business['_id'])
        for review in business['reviews']:
            review['_id'] = str(review['_id'])
        return make_response(jsonify(business), 200)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)


def add_new_business():
    if "name" in request.form and request.form["name"] != "":
        if "town" in request.form and request.form["town"] != "":
            if "rating" in request.form and request.form["rating"] != "":
                new_business = {"name": request.form["name"],
                                "town": request.form["town"],
                                "rating": request.form["rating"],
                                "reviews": []
                                }

                new_business_id = businesses.insert_one(new_business)
                new_business_link = "http://localhost:5000/api/v1.0/businesses/" \
                                    + str(new_business_id.inserted_id)
                return make_response(jsonify(
                    {"url": new_business_link}), 201)
            else:
                return make_response(jsonify({"error": "Missing rating data"}), 404)
        else:
            return make_response(jsonify({"error": "Missing town data"}), 404)
    else:
        return make_response(jsonify({"error": "Missing name data"}), 404)


def edit_business(id):
    if "name" and "town" and "rating" in request.form:
        result = businesses.update_one({"_id": ObjectId(id)}, {
            "$set": {"name": request.form["name"],
                     "town": request.form["town"],
                     "rating": request.form["rating"]
                     }
        })
        if result.matched_count == 1:
            edited_business_link = \
                "http://localhost:5000/api/v1.0/businesses/" + id
            return make_response(jsonify(
                {"url": edited_business_link}), 200)
        else:
            return make_response(jsonify({"error": "Invalid Business ID"}), 404)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 404)


def delete_business(id):
    result = businesses.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid Business ID"}), 404)
