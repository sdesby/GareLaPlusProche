#coding: utf-8

import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

import sys
sys.path.append(conf_parser.get("Path", "main_path"))

import math
from services import train_station_service

import garelaplusproche_logger as log

LOGGER = log.get_logger("garelaplusproche.engine")

def calculate_nearest_train_station(user_latitude, user_longitude, list_of_stations):
    LOGGER.info("Calculate Nearest station for coordinates: (" + str(user_latitude) + ", " + str(user_longitude)+ ")")
    shorter_distance = 99999999
    nearest_station = None

    for station in list_of_stations:
        current_distance = get_distance(user_latitude, user_longitude, station["latitude"], station["longitude"])

        if current_distance < shorter_distance:
            shorter_distance = current_distance
            nearest_station = station

    LOGGER.info("Found station: " + str(nearest_station))
    return nearest_station

def get_distance(user_latitude, user_longitude, other_latitude, other_longitude):
    earth_radius = 6371000.0

    user_lat_to_rad = math.radians(user_latitude)
    train_station_lat_to_rad = math.radians(other_latitude)

    delta_latitude = math.radians(other_latitude - user_latitude)
    delta_longitude = math.radians(other_longitude - user_longitude)

    a = math.sin(delta_latitude / 2) * math.sin(delta_latitude /2) \
    + math.cos(user_lat_to_rad) * math.cos(train_station_lat_to_rad) \
    * math.sin(delta_longitude / 2) * math.sin(delta_longitude /2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return (earth_radius * c) / 1000 #en km

def get_nearest_train_station(user_latitude, user_longitude):
    all_train_stations = train_station_service.get_all_train_stations()
    return calculate_nearest_train_station(user_latitude, user_longitude, all_train_stations)

def get_nearest_train_station_this_big(user_latitude, user_longitude, howbig):
    all_train_stations = train_station_service.get_all_train_stations_this_big(howbig)
    return calculate_nearest_train_station(user_latitude, user_longitude, all_train_stations)
