from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient("localhost", 27017)
    db = client['access']

    collection_token_to_expiration = db['token_to_expiration']
    collection_token_to_expiration.delete_many({})

    collection_id_to_password = db['id_to_password']
    collection_id_to_password.delete_many({})
    collection_id_to_password.insert_many([{
        'id': 'a',
        'password': 'Xksnfodaso'
    }])

    collection_id_to_publicKey = db['id_to_publicKey']
    collection_id_to_publicKey.delete_many({})

    client.close()
