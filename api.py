#coding: utf-8

from flask import Flask
from flask_restful import Api, Resource
from webargs import fields
from webargs.flaskparser import use_args
import json
from bson import json_util

import engine
from geocode import Geocode

app = Flask(__name__)
api = Api(app)

address = {
"number": fields.Str(missing=""),
"street": fields.Str(required=True),
"postalcode": fields.Str(missing=None),
"city": fields.Str(required=True)
}

def address_to_string(address):
    result = address["number"] + " " + address["street"] + ", ";
    if address["postalcode"] is not None:
        result += address["postalcode"] + " " + address["city"]
    else:
        result +=  address["city"]
    return result

class Distance(Resource):

    coordinates = {
    'x1': fields.Float(missing=0.0),
    'y1': fields.Float(missing=0.0),
    'x2': fields.Float(missing=0.0),
    'y2': fields.Float(missing=0.0)
    }

    @use_args(coordinates)
    def get(self, args):
        distance = engine.get_distance(args['x1'], args['y1'], args['x2'], args['y2'])
        return {"distance": distance}

class Coordinates(Resource):

    @use_args(address)
    def get(self, args):
        geocode = Geocode()
        address = address_to_string(args)
        result = geocode.get_coordinates_from_address(address)

        return result

class NearestStation(Resource):

    @use_args(address)
    def get(self, args):
        geocode = Geocode()
        coordinates = geocode.get_coordinates_from_address(address_to_string(args))
        nearest_station = engine.get_nearest_train_station(float(coordinates[0]["geometry"]["lat"]), float(coordinates[0]["geometry"]["lng"]))
        return json.loads(json_util.dumps(nearest_station))

api.add_resource(Distance, "/distance")
api.add_resource(Coordinates, "/coordinates")
api.add_resource(NearestStation, "/nearest-station")

if __name__ == '__main__':
    app.run(debug=True)
