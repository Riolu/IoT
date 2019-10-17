from pymongo import MongoClient

DB_NAME = "columbia"
URLS = [
    {"loc": "master", "url": "http://192.168.1.189:5000"},
    {"loc": "parent", "url": "http://192.168.1.189:5000"},
    {"loc": "self", "url": "columbia"},
    {"loc": "irt", "url": "http://192.168.1.156:5002"},
    {"loc": "cs", "url": "http://192.168.1.156:5003"}
]

client = MongoClient("localhost", 27017)
db = client[DB_NAME]

collection_loc_to_url = db["loc_to_url"]
collection_loc_to_url.delete_many({})
collection_loc_to_url.insert_many(URLS)

client.close()
