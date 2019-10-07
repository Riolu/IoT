from pymongo import MongoClient

DB_NAME = "manhattan"
URLS = [
    {"master": "http://localhost:5000"},
    {"parent": ""},
    {"columbia": "http://localhost:5001"}
]

client = MongoClient("localhost", 27017)
db = client[DB_NAME]

collection_loc_to_url = db["loc_to_url"]
collection_loc_to_url.insert_many(URLS)

client.close()
