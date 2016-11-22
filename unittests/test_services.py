#coding: utf-8

import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

import sys
sys.path.append(conf_parser.get("Path", "main_path"))

######################

import unittest
from services import train_station_service

class TestTrainStationService(unittest.TestCase):

    def test_get_all_train_stations(self):
        all_train_stations = train_station_service.get_all_train_stations()
        self.assertEqual(all_train_stations.count(), 2973)

    def test_get_only_stations_of_given_size(self):
        #should return stations where howbig = a
        a_big_stations = train_station_service.get_all_train_stations_this_big("a")
        for station in a_big_stations:
            self.assertEqual(station["howbig"], "a")

        #should return stations where howbig = b
        b_big_stations = train_station_service.get_all_train_stations_this_big("b")
        for station in b_big_stations:
            self.assertEqual(station["howbig"], "b")

        #should return stations where howbig = a b
        ab_big_stations = train_station_service.get_all_train_stations_this_big("a b")
        for station in ab_big_stations:
            self.assertEqual(station["howbig"], "a b")

        #should return stations where howbig = b
        c_big_stations = train_station_service.get_all_train_stations_this_big("c")
        for station in c_big_stations:
            self.assertEqual(station["howbig"], "c")

if __name__ == "__main__":
    unittest.main()
