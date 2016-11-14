#coding: utf-8

from opencage.geocoder import OpenCageGeocode
import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

class Geocode:

    def __init__(self):
        self.geocoder = OpenCageGeocode(conf_parser.get("Geocode", "key"))

    def get_coordinates_from_address(self, address):
        result = self.geocoder.geocode(address, format="json", language="fr")
        if result == []:
            return None
        else:
            return result
