#coding: utf-8

import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

import sys
sys.path.append(conf_parser.get("Path", "main_path"))

import math
from services import train_station_service

def get_distance(x1, y1, x2, y2):
    earth_radius = 6371000.0

    user_lat_to_rad = math.radians(x1)
    train_station_lat_to_rad = math.radians(x2)

    delta_latitude = math.radians(x2 - x1)
    delta_longitude = math.radians(y2 - y1)

    a = math.sin(delta_latitude / 2) * math.sin(delta_latitude /2) \
    + math.cos(user_lat_to_rad) * math.cos(train_station_lat_to_rad) \
    * math.sin(delta_longitude / 2) * math.sin(delta_longitude /2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round((earth_radius * c) / 1000, 2) #en km

def get_nearest_train_station(x1, y1):
    shorter_distance = 99999999
    all_train_stations = train_station_service.get_all_train_stations()

    nearest_station = None

    for i in all_train_stations:
        current_distance = get_distance(x1, y1, i["latitude"], i["longitude"])

        if current_distance < shorter_distance:
            shorter_distance = current_distance
            nearest_station = i

    return nearest_station
