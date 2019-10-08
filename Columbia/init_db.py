from pymongo import MongoClient

DB_NAME = "columbia"
URLS = [
    {"loc": "master", "url": "http://localhost:5000"},
    {"loc": "parent", "url": "http://localhost:5000"},
    {"loc": "self", "url": "columbia"}
]

client = MongoClient("localhost", 27017)
db = client[DB_NAME]

collection_loc_to_url = db["loc_to_url"]
collection_loc_to_url.delete_many({})
collection_loc_to_url.insert_many(URLS)

client.close()
