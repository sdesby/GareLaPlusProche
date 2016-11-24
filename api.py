#coding: utf-8

from flask import Flask
from flask_restful import Api, Resource
from webargs import fields
from webargs.flaskparser import use_args
import json
from bson import json_util

import engine
from geocode import Geocode
from dao import database
from pymongo import errors

app = Flask(__name__)
api = Api(app)

address = {
"address": fields.Str(required=True),
"howbig": fields.Str(missing="")
}

detailed_address = {
"number": fields.Str(missing=""),
"street": fields.Str(required=True),
"postalcode": fields.Str(missing=None),
"city": fields.Str(required=True),
"howbig": fields.Str(missing="")
}

def address_to_string(detailed_address):
    result = detailed_address["number"] + " " + detailed_address["street"] + ", ";
    if detailed_address["postalcode"] is not None:
        result += detailed_address["postalcode"] + " " + detailed_address["city"]
    else:
        result +=  detailed_address["city"]
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

    @use_args(detailed_address)
    def get(self, args):
        geocode = Geocode()
        detailed_address = address_to_string(args)
        result = geocode.get_coordinates_from_address(detailed_address)

        return result

class NearestStations(Resource):

    @use_args(address)
    def get(self, args):
        geocode = Geocode()
        coordinates = geocode.get_coordinates_from_address(args["address"])

        if args["howbig"] == "":
            nearest_station = engine.get_nearest_train_station(float(coordinates[0]["geometry"]["lat"]), float(coordinates[0]["geometry"]["lng"]))
        else:
            nearest_station = engine.get_nearest_train_station_this_big(float(coordinates[0]["geometry"]["lat"]), float(coordinates[0]["geometry"]["lng"]), args["howbig"])
        return json.loads(json_util.dumps(nearest_station))

class NearestStationDetailedAddress(Resource):

    @use_args(detailed_address)
    def get(self, args):
        geocode = Geocode()
        coordinates = geocode.get_coordinates_from_address(address_to_string(args))
        if args["howbig"] == "":
            nearest_station = engine.get_nearest_train_station(float(coordinates[0]["geometry"]["lat"]), float(coordinates[0]["geometry"]["lng"]))
        else:
            nearest_station = engine.get_nearest_train_station_this_big(float(coordinates[0]["geometry"]["lat"]), float(coordinates[0]["geometry"]["lng"]), args["howbig"])
        return json.loads(json_util.dumps(nearest_station))

api.add_resource(Distance, "/distance")
api.add_resource(Coordinates, "/coordinates")
api.add_resource(NearestStations, "/nearest-station")
api.add_resource(NearestStationDetailedAddress, "/nearest-station-detailed-address")

if __name__ == '__main__':
    #Before all, testing database connection:
    try:
        db = database.Database()
        db.client.server_info()
        app.run(debug=True)
    except errors.ServerSelectionTimeoutError:
        print "Sorry, can't connect to database"
