from flask import Flask, jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# initialize flask
app = Flask(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'cDB.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize Database
db = SQLAlchemy(app)
# init marshmallow
ma = Marshmallow(app)



# car class
class Vehicle(db.Model):
    makeID = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(200))
    status = db.Column(db.String(200))

    def __init__(self, manufacturer, status):
        self.manufacturer = manufacturer
        self.status = status
        


# Vehicle Schema 
class VehicleSchema(ma.Schema):
    class Meta:
        fields = ('makeID', 'manufacturer', 'status')



# intitialize schema
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)



# create a car entry POST
@app.route('/vehicle', methods=['POST'])
def add_car():
    manufacturer = request.json['manufacturer']
    status = request.json['status']

    new_vehicle = Vehicle(manufacturer,status)

    db.session.add(new_vehicle)
    db.session.commit()

    return vehicle_schema.jsonify(new_vehicle)



@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    all_vehicles = Vehicle.query.all()
    result = vehicles_schema.dump(all_vehicles)
    return jsonify(result.data)










# # serialize json data to correct format
# def serialize():
#     data = {
#         "makeID": {
#             "manufacturer"
#             "model"
#             "color"
#             "style"
#         }
#     }
#     with open("data_file.json", "w") as write_file:
#         json.dump(data, write_file, indent=4)
#     json_str = json.dumps(data, indent=4)
#     print(json_str)



# @app.route('/')
# def homepage():
#     return 'howdy, welcome to the home page'



# @app.errorhandler(404)
# def page_not_found(e):
#     return 'This is not the page you are looking for'

# Run server
if __name__ == "__main__":
    app.run(debug=True)
