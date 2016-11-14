#coding: utf-8

import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

import sys
sys.path.append(conf_parser.get("Path", "main_path"))

import unittest
import engine
from geocode import Geocode

class TestGeocode(unittest.TestCase):

    def test_should_return_coordinates(self):
        """
        Saint Quentin le verger :
        x1 = 48.619380
        y1 = 3.746980
        """
        geocode = Geocode()

        address = "14 rue de Vignolle, Saint-Quentin-le-verger"
        result = geocode.get_coordinates_from_address(address)

        latitude = str(result[0]["geometry"]["lat"])
        longitude = str(result[0]["geometry"]["lng"])

        distance = engine.get_distance(float(latitude), float(longitude), 48.619380, 3.746980)

        self.assertLess(distance, 0.5)

if __name__ == '__main__':
    unittest.main()
