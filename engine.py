#coding: utf-8

import math

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
