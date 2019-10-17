from pymongo import MongoClient

DB_NAME = "irt"
URLS = [
    {"loc": "master", "url": "http://192.168.1.189:5000"},
    {"loc": "parent", "url": "http://192.168.1.156:5001"},
    {"loc": "self", "url": "irt"}
]

client = MongoClient("localhost", 27017)
db = client[DB_NAME]

collection_loc_to_url = db["loc_to_url"]
collection_loc_to_url.delete_many({})
collection_loc_to_url.insert_many(URLS)

client.close()
