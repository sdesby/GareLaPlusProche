from pymongo import MongoClient
import os


class Database:

    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGODB_URI'))
        self.db = self.client[os.environ.get('DB_NAME')]
        self.train_station_collection = self.db[os.environ.get('DB_COLLECTION')]

    @property
    def client(self):
        return self.client

    @property
    def db(self):
        return self.db

    @property
    def train_station_collection(self):
        return self.train_station_collection
