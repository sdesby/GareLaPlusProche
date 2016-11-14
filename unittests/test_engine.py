#coding: utf-8

import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

import sys
sys.path.append(conf_parser.get("Path", "main_path"))
import unittest
import engine


class TestGetDistance(unittest.TestCase):

    def test_should_return_zero(self):
        #should return 0
        self.assertEqual(engine.get_distance(0,0,0,0), 0)

    def test_get_distance_btw_home_sqlv(self):
        #should return 103.50408330561693
        distance_to_find = 103.50
        """
        Saint Quentin le verger :
        x1 = 48.619380
        y1 = 3.746980

        2 rue Gobert, Paris :
        x2 = 48.855698
        y2 = 2.381795
        """
        self.assertEqual(engine.get_distance(48.619380, 3.746980, 48.855698, 2.381795), distance_to_find)

if __name__ == '__main__':
    unittest.main()
