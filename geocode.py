#coding: utf-8

from opencage.geocoder import OpenCageGeocode
import os

class Geocode:

    def __init__(self):
        self.geocoder = OpenCageGeocode(os.environ.get('GEOCODE'))

    def get_coordinates_from_address(self, address):
        result = self.geocoder.geocode(address, format="json", language="fr")
        if result == []:
            return None
        else:
            return result
