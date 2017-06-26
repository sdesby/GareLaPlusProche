#coding: utf-8

from dao.database import Database


def get_all_train_stations():
    return Database().train_station_collection.find()


def get_nearest_train_station(user_latitude, user_longitude):
    return Database().train_station_collection.find({"$and": [{"geometry": {"$near": {"$geometry": {"type": "Point", "coordinates":[user_longitude, user_latitude]},"$maxDistance": 70000} }}, {"properties.voyageurs": "O"}]});
