#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurants_data = [restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants]
    return jsonify(restaurants_data), 200

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = db.session.get(Restaurant, id)

    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurant_data = restaurant.to_dict()
    return jsonify(restaurant_data), 200
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    


    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizzas_data = [pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas]
    return jsonify(pizzas_data), 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    
    # Validate price
    if data['price'] < 1 or data['price'] > 30:
        return jsonify({"errors": ["validation errors"]}), 400


    restaurant = db.session.get(Restaurant, data['restaurant_id'])
    pizza = db.session.get(Pizza, data['pizza_id'])
    if not restaurant or not pizza:
        return jsonify({"errors": ["Invalid restaurant or pizza"]}), 400

    # Create new restaurant_pizza
    restaurant_pizza = RestaurantPizza(price=data['price'], restaurant_id=restaurant.id, pizza_id=pizza.id)
    db.session.add(restaurant_pizza)
    db.session.commit()

    
    response_data = restaurant_pizza.to_dict()
    return jsonify(response_data), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404







if __name__ == '__main__':
    app.run(port=5555, debug=True)
