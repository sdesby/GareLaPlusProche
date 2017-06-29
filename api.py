# coding: utf-8

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

nearest_station_args = {
    "address": fields.Str(required=True),
    "maxdistance": fields.Str(missing="50")
}

detailed_address = {
    "number": fields.Str(missing=""),
    "street": fields.Str(required=True),
    "postalcode": fields.Str(missing=None),
    "city": fields.Str(required=True),
}


def address_to_string(address):
    result = address["number"] + " " + address["street"] + ", ";
    if address["postalcode"] is not None:
        result += address["postalcode"] + " " + address["city"]
    else:
        result += address["city"]
    LOGGER.info("Built address \"" + result + "\" from detailed address")
    return result


class Coordinates(Resource):
    @use_args(detailed_address)
    def get(self, args):
        geocode = Geocode()
        detailed_address = address_to_string(args)
        result = geocode.get_coordinates_from_address(detailed_address)

        return result


class NearestStations(Resource):
    @use_args(nearest_station_args)
    def get(self, args):
        geocode = Geocode()
        address = args["address"]
        complete_json_answer_for_address = geocode.get_coordinates_from_address(address)

        if complete_json_answer_for_address is not None:
            latitude = float(complete_json_answer_for_address[0]["geometry"]["lat"])
            longitude = float(complete_json_answer_for_address[0]["geometry"]["lng"])
            LOGGER.info("Coordinates for address \"" + address + "\" are: " + str(latitude) + "," + str(longitude))
            nearest_station = engine.get_nearest_train_station(latitude, longitude, args["maxdistance"])
            return json.loads(json_util.dumps(nearest_station, ensure_ascii=False).encode('utf8'))
        else:
            LOGGER.error("No answer from OpenCageGeocode for address: \"" + address + "\"")
            return json.loads(
                "{\"error\": {\"message\": \"Bad request. Check if address exists\", \"status\": 400}}"), 400


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
            nearest_station = engine.get_nearest_train_station(latitude, longitude)
            return json.loads(json_util.dumps(nearest_station))
        else:
            LOGGER.error("No answer from OpenCageGeocode for address: \"" + address + "\"")
            return json.loads(
                "{\"error\": {\"message\": \"Bad request. Check if address exists\", \"status\": 400}}"), 400


api.add_resource(Coordinates, "/coordinates")
api.add_resource(NearestStations, "/nearest-station")
api.add_resource(NearestStationDetailedAddress, "/nearest-station-detailed-address")

if __name__ == '__main__':
    LOGGER.info("***** App launched ! *****")
    # Before all, testing database connection:
    try:
        db = database.Database()
        db.client.server_info()
        port = int(os.environ.get('PORT', 5000))
        LOGGER.info("I found PORT number: " + str(port))
        app.run(host='0.0.0.0', port=port)
    except errors.ServerSelectionTimeoutError:
        LOGGER.error("Sorry, can't connect to database")
