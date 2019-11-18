from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient("localhost", 27017)
    db = client['access']

    collection_token_to_expiration = db['token_to_expiration']
    collection_token_to_expiration.delete_many({})

    client.close()
