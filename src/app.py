from flask import Flask, request, jsonify, make_response
from controller.businessController import business_controller_blueprint
from controller.reviewController import review_controller_blueprint

from utils import Utils

app = Flask(__name__)
app.register_blueprint(business_controller_blueprint)
app.register_blueprint(review_controller_blueprint)
app.config['SECRET_KEY'] = 'mysecret'

if __name__ == "__main__":
    businesses = Utils.generate_dummy_data()
    app.run(debug=True)
