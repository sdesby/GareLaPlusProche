#coding: utf-8

import math
from services import train_station_service

import garelaplusproche_logger as log

LOGGER = log.get_logger("garelaplusproche.engine")

def get_nearest_train_station(user_latitude, user_longitude):
    return train_station_service.get_nearest_train_station(user_latitude, user_longitude)
