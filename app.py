from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# initialize application
app = Flask(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))


# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'carDB.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialization of Database
db = SQLAlchemy(app)

#initialization of marshmallow serializer
ma = Marshmallow(app)

# class for cars
# can go into separate file for Models
class Vehicle(db.Model):
  makeID = db.Column(db.Integer, primary_key=True)
  make = db.Column(db.String(20))
  model = db.Column(db.String(20), unique=True)
  price = db.Column(db.Integer, default=20)
  
  # constructor for vehicle class
  def __init__(self, make, model, price):
    self.make = make
    self.model = model
    self.price = price



# vehicle Schema
class VehicleSchema(ma.Schema):
  class Meta:
    fields = ('makeID','make', 'model', 'price')

# initialize Schema
vehicle_schema = VehicleSchema(strict = True)
vehicles_schema = VehicleSchema(many = True, strict = True)



# Create a vehicle
@app.route('/vehicle', methods=['POST'])
def add_car():
  make = request.json['make']
  model = request.json['model']
  price = request.json['price']

  new_vehicle = Vehicle(make, model, price)

  db.session.add(new_vehicle)
  db.session.commit()

  return vehicle_schema.jsonify(new_vehicle)

# return all vehicles
@app.route('/vehicle', methods=['GET'])
def get_AllCars():
  all_cars = Vehicle.query.all()
  result = vehicles_schema.dump(all_cars)
  return jsonify(result.data)

# return one vehicle
@app.route('/vehicle/<makeID>',methods=['GET'])
def get_car(makeID):
  car = Vehicle.query.get(makeID)
  return vehicle_schema.jsonify(car)


# update a vehicle
@app.route('/vehicle/<makeID>', methods=['PUT'])
def update_car(makeID):
  car = Vehicle.query.get(makeID)
  make = request.json['make']
  model = request.json['model']
  price = request.json['price']

  car.make = make
  car.model = model
  car.price = price

  db.session.commit()

  return vehicle_schema.jsonify(car)


# Delete vehicle
@app.route('/vehicle/<makeID>',methods=['DELETE'])
def delete_car(makeID):
  car = Vehicle.query.get(makeID)
  db.session.delete(car)
  db.session.commit()
  return vehicle_schema.jsonify(car)






#Run Server
if __name__ == '__main__':
  app.run(debug=True)
