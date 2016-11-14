from pymongo import MongoClient
import ConfigParser

conf_parser = ConfigParser.ConfigParser()
conf_parser.read("./config.properties")

class Database:

    def __init__(self):
        self.client = MongoClient(conf_parser.get("DB", "host"), conf_parser.getint("DB", "port"))
        self.db = self.client[conf_parser.get("DB", "db_name")]

    @property
    def client(self):
        return self.client

    @property
    def db(self):
        return self.db
