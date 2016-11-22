#coding: utf-8

import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

import sys
sys.path.append(conf_parser.get("Path", "main_path"))

from dao.database import Database

def get_all_train_stations():
    return Database().train_station_collection.find()

def get_all_train_stations_this_big(howbig):
    return Database().train_station_collection.find({"howbig": howbig})
