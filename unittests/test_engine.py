#coding: utf-8

import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

import sys
sys.path.append(conf_parser.get("Path", "main_path"))
import unittest
import engine

"""
Saint Quentin le verger (sqlv):
x1 = 48.619380
y1 = 3.746980

2 rue Gobert, Paris (home):
x2 = 48.855698
y2 = 2.381795
"""

class TestGetDistance(unittest.TestCase):

    def test_should_return_zero(self):
        #should return 0
        self.assertEqual(engine.get_distance(0,0,0,0), 0)

    def test_get_distance_btw_home_sqlv(self):
        #should return 103.50408330561693
        distance_to_find = 103.50408330561693

        self.assertEqual(engine.get_distance(48.619380, 3.746980, 48.855698, 2.381795), distance_to_find)

    def test_get_nearest_station_of_home(self):
        #should return Gare de Lyon train station
        actual_station = engine.get_nearest_train_station(48.855698, 2.381795)
        self.assertEqual(actual_station["name"], "Paris Gare de Lyon")

    def test_get_nearest_station_of_sqlv_big_as_a(self):
        #should return Champagne Ardennes TGV train station
        actual_station = engine.get_nearest_train_station_this_big(48.619380, 3.746980, "a")
        self.assertEqual(actual_station["name"], "Champagne Ardennes TGV")

    def test_get_nearest_station_of_sqlv_big_as_a(self):
        #should return Romilly-sur-Seine train station
        actual_station = engine.get_nearest_train_station_this_big(48.619380, 3.746980, "b")
        self.assertEqual(actual_station["name"], "Romilly-sur-Seine")

if __name__ == '__main__':
    unittest.main()
