from pymongo import MongoClient

DB_NAME = "manhattan"
URLS = [
    {"loc": "master", "url": "http://192.168.1.189:5000"},
    {"loc": "parent", "url": ""},
    {"loc": "columbia", "url": "http://192.168.1.156:5001"},
    {"loc": "self", "url": "manhattan"}
]

CHILD_LOCS = [
        {"targetLoc": "irt", "childLoc": "columbia"},
        {"targetLoc": "cs", "childLoc": "columbia"}
    ]

def dbinit(dbname, urls, child_locs, drop=False):
    client = MongoClient("localhost", 27017)
    if drop:
        client.drop_databse(dbname)
    db = client[dbname]

    collection_loc_to_url = db["loc_to_url"]
    collection_loc_to_url.delete_many({})
    collection_loc_to_url.insert_many(urls)

    collection_targetLoc_to_childLoc = db["targetLoc_to_childLoc"]
    collection_targetLoc_to_childLoc.delete_many({})
    collection_targetLoc_to_childLoc.insert_many(child_locs)

    client.close()
