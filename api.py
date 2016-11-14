#coding: utf-8

from flask import Flask
from flask_restful import Api, Resource
from webargs import fields
from webargs.flaskparser import use_args
import engine
from geocode import Geocode

app = Flask(__name__)
api = Api(app)

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

    address = {
    "number": fields.Str(missing=""),
    "street": fields.Str(required=True),
    "postalcode": fields.Str(missing=None),
    "city": fields.Str(required=True)
    }

    @use_args(address)
    def get(self, args):
        geocode = Geocode()
        address = args["number"] + " " + args["street"] + ", ";
        if args["postalcode"] is not None:
            address += args["postalcode"] + " " + args["city"]
        else:
            address +=  args["city"]
        result = geocode.get_coordinates_from_address(address)

        return result

api.add_resource(Distance, "/distance")
api.add_resource(Coordinates, "/coordinates")

if __name__ == '__main__':
    app.run(debug=True)
