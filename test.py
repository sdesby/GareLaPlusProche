from pymongo import MongoClient

client = MongoClient("mongodb://<user>:<password>@<host>:<port>/<dbname>")
db = client["<dbname>"]
train_station_collection = db["<collectionname>"]

print train_station_collection.count()

latitude = 48.619380
longitude = 3.746980

stations =  train_station_collection.find({"geometry": {"$near": {"$geometry": {"type": "Point", "coordinates":[3.746980,48.619380]},"$maxDistance": 70000} }});

for s in stations:
    if s["properties"]["voyageurs"] == "O":
        print s["properties"]["commune"].encode("utf-8")
