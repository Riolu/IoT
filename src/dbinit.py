import argparse
from pymongo import MongoClient

def dbinit(dbname, urls, child_locs, drop=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--drop', dest='drop', action='store_true')
    parser.set_defaults(drop=False)
    args = parser.parse_args()

    client = MongoClient("localhost", 27017)
    if args.drop:
        client.drop_databse(dbname)
    db = client[dbname]

    collection_loc_to_url = db["loc_to_url"]
    collection_loc_to_url.delete_many({})
    if urls:
        collection_loc_to_url.insert_many(urls)

    collection_targetLoc_to_childLoc = db["targetLoc_to_childLoc"]
    collection_targetLoc_to_childLoc.delete_many({})
    if child_locs:
        collection_targetLoc_to_childLoc.insert_many(child_locs)

    client.close()
