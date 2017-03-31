#coding: utf-8

from flask import Flask
from flask_restful import Api, Resource
from webargs import fields
from webargs.flaskparser import use_args
import json
from bson import json_util
import os

import engine
from geocode import Geocode
from dao import database
from pymongo import errors

import garelaplusproche_logger as log

LOGGER = log.get_logger("garelaplusproche")

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
    LOGGER.info("Built address \"" + result + "\" from detailed address")
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
        address = args["address"]
        complete_json_answer_for_address = geocode.get_coordinates_from_address(address)

        if complete_json_answer_for_address is not None:
            latitude = float(complete_json_answer_for_address[0]["geometry"]["lat"])
            longitude = float(complete_json_answer_for_address[0]["geometry"]["lng"])
            LOGGER.info("Coordinates for address \"" + address + "\" are: " + str(latitude) + "," + str(longitude))
            if args["howbig"] == "":
                nearest_station = engine.get_nearest_train_station(latitude, longitude)
            else:
                nearest_station = engine.get_nearest_train_station_this_big(latitude, longitude)
            return json.loads(json_util.dumps(nearest_station, ensure_ascii=False).encode('utf8'))
        else:
            LOGGER.error("No answer from OpenCageGeocode for address: \"" + address + "\"")
            return json.loads("{\"error\": {\"message\": \"Bad request. Check if address exists\", \"status\": 400}}"), 400

class NearestStationDetailedAddress(Resource):

    @use_args(detailed_address)
    def get(self, args):
        geocode = Geocode()
        address = address_to_string(args)
        complete_json_answer_for_address = geocode.get_coordinates_from_address(address)

        if complete_json_answer_for_address is not None:
            latitude = float(complete_json_answer_for_address[0]["geometry"]["lat"])
            longitude = float(complete_json_answer_for_address[0]["geometry"]["lng"])
            LOGGER.info("Coordinates for address \"" + address + "\" are: " + str(latitude) + "," + str(longitude))
            if args["howbig"] == "":
                nearest_station = engine.get_nearest_train_station(latitude, longitude)
            else:
                nearest_station = engine.get_nearest_train_station_this_big(latitude, longitude)
            return json.loads(json_util.dumps(nearest_station))
        else:
            LOGGER.error("No answer from OpenCageGeocode for address: \"" + address + "\"")
            return json.loads("{\"error\": {\"message\": \"Bad request. Check if address exists\", \"status\": 400}}"), 400

api.add_resource(Distance, "/distance")
api.add_resource(Coordinates, "/coordinates")
api.add_resource(NearestStations, "/nearest-station")
api.add_resource(NearestStationDetailedAddress, "/nearest-station-detailed-address")

if __name__ == '__main__':
    LOGGER.info("***** App launched ! *****")
    #Before all, testing database connection:
    try:
        db = database.Database()
        db.client.server_info()
        port = int(os.environ.get('PORT', 5000))
        LOGGER.info("I found PORT number: " + str(port))
        app.run(host='0.0.0.0', port=port)
    except errors.ServerSelectionTimeoutError:
        LOGGER.error("Sorry, can't connect to database")
