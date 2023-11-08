import random
import uuid

from flask import Flask, request, jsonify, make_response

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


