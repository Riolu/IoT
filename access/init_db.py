from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient("localhost", 27017)
    db = client['access']

    collection_loc_to_url = db['loc_to_url']
    collection_loc_to_url.delete_many({})
    collection_loc_to_url.insert_many([
        {'loc': 'master', 'url': 'http://192.168.1.189:5000/'}
    ])

    collection_revoked_ = db['']


    client.close()

