#coding: utf-8

import math
from services import train_station_service

import garelaplusproche_logger as log

LOGGER = log.get_logger("garelaplusproche.engine")

def get_nearest_train_station(user_latitude, user_longitude):
    return train_station_service.get_nearest_train_station(user_latitude, user_longitude)


def get_nearest_train_station_this_big(user_latitude, user_longitude, howbig):
    all_train_stations = train_station_service.get_all_train_stations_this_big(howbig)
    return calculate_nearest_train_station(user_latitude, user_longitude, all_train_stations)
