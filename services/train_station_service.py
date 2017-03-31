#coding: utf-8

from dao.database import Database

def get_all_train_stations():
    return Database().train_station_collection.find()

def get_all_train_stations_this_big(howbig):
    return Database().train_station_collection.find({"howbig": howbig})
