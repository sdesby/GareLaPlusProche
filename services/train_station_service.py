#coding: utf-8

from dao.database import Database


def get_all_train_stations():
    return Database().train_station_collection.find()


def get_nearest_train_station(user_latitude, user_longitude):
    return Database().train_station_collection.find({"$and": [{"geometry": {"$near": {"$geometry": {"type": "Point", "coordinates":[3.746980, 48.619380]},"$maxDistance": 70000} }}, {"properties.voyageurs": "O"}]});


def get_all_train_stations_this_big(howbig):
    return Database().train_station_collection.find({"howbig": howbig})
