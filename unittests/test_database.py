#coding: utf-8

import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

import sys
sys.path.append(conf_parser.get("Path", "main_path"))

import unittest
from pymongo import MongoClient
from pymongo import database as db_mongo
from dao.database import Database

class TestDatabase(unittest.TestCase):

    def test_should_return_a_train_station(self):
        database = Database()
        self.assertEqual(type(database.client), MongoClient)
        self.assertEqual(type(database.db), db_mongo.Database)

if __name__ == "__main__":
    unittest.main()
