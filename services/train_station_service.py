#coding: utf-8
import garelaplusproche_logger as log
from dao.database import Database

LOGGER = log.get_logger("garelaplusproche.service")

def get_all_train_stations():
    return Database().train_station_collection.find()


def get_nearest_train_station(user_latitude, user_longitude, maxdistance):
    max_distance = int(maxdistance) * 1000
    LOGGER.info("Max Distance: " + str(max_distance))
    return Database().train_station_collection.find({"$and": [{"geometry": {"$near": {"$geometry": {"type": "Point", "coordinates":[user_longitude, user_latitude]},"$maxDistance": max_distance}}}, {"properties.voyageurs": "O"}]});
