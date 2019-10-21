from pymongo import MongoClient

DB_NAME = "manhattan"
URLS = [
    {"loc": "master", "url": "http://192.168.1.189:5000"},
    {"loc": "parent", "url": ""},
    {"loc": "columbia", "url": "http://192.168.1.156:5001"},
    {"loc": "self", "url": "manhattan"}
]

def init_db(dbname, urls, drop=False):

    client = MongoClient("localhost", 27017)
    db = client[dbname]

    collection_loc_to_url = db["loc_to_url"]
    collection_loc_to_url.delete_many({})
    collection_loc_to_url.insert_many(urls)

    child_locs = [
        {"targetLoc": "irt", "childLoc": "columbia"},
        {"targetLoc": "cs", "childLoc": "columbia"}
    ]

    collection_targetLoc_to_childLoc = db["targetLoc_to_childLoc"]
    collection_targetLoc_to_childLoc.delete_many({})
    collection_targetLoc_to_childLoc.insert_many(child_locs)

    client.close()
