import json
import re
from .config import Config
from flask import Flask, request, Response
from pymongo import MongoClient
import jwt
import requests
import datetime
import time
from jwt.exceptions import DecodeError
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode, b64decode

'''
type = tv
check all match
check exact match

json = {
    'id': ['x', 'y', 'z'], // child in the end
    'permission': {
        'resource': 'searchByLocType',
        'params': {
            'loc': 'col',
            'type': '*'
        }
    }
}

operation = {
    'resource': 'searchByLocType',
    'method': 'GET',
    'params': {},
    'data': {}
}
'''

def rsa_verify(signature, _id, publicKey):
    sign = b64decode(signature)
    h = SHA.new(_id.encode('utf-8'))
    # keyDER = b64decode(privateKey)
    keyPub = RSA.importKey(publicKey)
    verifier = PKCS1_v1_5.new(keyPub)
    return verifier.verify(h, sign)


def isSatisfiable(operation_permission, decoded_permission):
    if operation_permission['resource'] != decoded_permission['resource']:
        return False
    for key, value in operation_permission['params'].items():
        if key not in decoded_permission['params'] or (
                value != decoded_permission['params'][key]
                and decoded_permission['params'][key] != '*'):
            return False
    return True


def isStaleToken(token):
    db_name = 'access'
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db['token_to_expiration']

    token_expiration = collection.find_one({'token': token})
    client.close()
    return token_expiration is not None and token_expiration[
        'expiration'] < time.time()


def verify(token, secret, operation):
    decoded = jwt.decode(token, secret, algorithm='HS256')
    decoded_permission = decoded['permission']
    operation_permission = {
        key: operation[key]
        for key in ['resource', 'params']
    }
    if isStaleToken(token):
        return False
    return isSatisfiable(operation_permission, decoded_permission)


def _requestToken(secret, permission, _id):
    encoded = jwt.encode({
        'id': _id,
        'permission': permission
    },
                         secret,
                         algorithm='HS256').decode('ascii')
    return encoded


if __name__ == '__main__':

    app = Flask("access")
    app.config.from_object(Config)
    SECRET = app.config['SECRET']
    MASTER_URL = app.config['MASTER_URL']

    @app.route('/registerUserPublicKey', methods=['POST'])
    def registerUserPublicKey():
        body = request.get_json()
        try:
            publicKey = body['publicKey']
            _id = body['id']
            password = body['password']
        except KeyError:
            return Response("Bad request data", status=400)

        db_name = 'access'
        client = MongoClient('localhost', 27017)
        db = client[db_name]
        id_to_password_collection = db['id_to_password']
        password_item = id_to_password_collection.find_one({'id': _id})
        if password_item is None or password_item['password'] != password:
            return Response("Authentication error", status=403)

        id_to_publicKey_collection = db['id_to_publicKey']

        if id_to_publicKey_collection.find_one({'id': _id}) is not None:
            id_to_publicKey_collection.update({'id': _id}, {
                'id': _id,
                'publicKey': publicKey
            })
        else:
            id_to_publicKey_collection.insert_one({'id': _id, 'publicKey': publicKey})
        client.close()

        return {}

    @app.route('/request', methods=['POST'])
    def requestToken():
        body = request.get_json()
        try:
            adminId = body['adminId']
            password = body['password']
            userId = body['userId']
            permission = body['permission']
        except KeyError:
            return Response("Bad request data", status=400)

        db_name = 'access'
        client = MongoClient('localhost', 27017)
        db = client[db_name]
        admin_to_password_collection = db['admin_to_password']
        password_item = admin_to_password_collection.find_one({'id': adminId})
        if password_item is None or password_item['password'] != password:
            return Response("Authentication error", status=403)

        token = _requestToken(SECRET, permission, [userId])
        collection = db['token_to_expiration']
        if collection.find_one({'token': token}) is not None:
            collection.delete_one({'token': token})
        client.close()

        return token

    @app.route('/revoke', methods=['POST'])
    def revoke():
        body = request.get_json()
        try:
            _id = body['id']
            token = body['token']
            signature = body['signature']
        except KeyError:
            return Response("Bad request data", status=400)

        # from database get corresponding public key
        db_name = 'access'
        client = MongoClient('localhost', 27017)
        db = client[db_name]
        collection = db['id_to_publicKey']
        pubkey_item = collection.find_one({'id': _id})
        if pubkey_item is None:
            return Response("User not registered", status=403)
        
        publicKey = pubkey_item['publicKey']
        if not rsa_verify(signature, _id, publicKey):
            return Response("Authentication error", status=403)

        db_name = 'access'
        client = MongoClient('localhost', 27017)
        db = client[db_name]
        collection = db['token_to_expiration']

        if collection.find_one({'token': token}) is not None:
            collection.update({'token': token}, {
                'token': token,
                'expiration': time.time()
            })
        else:
            collection.insert_one({'token': token, 'expiration': time.time()})
        client.close()
        return {}


    @app.route('/delegate', methods=['POST'])
    def delegate():
        body = request.get_json()
        try:
            token = body['token']
            childID = body['childID']
            _id = body['id']
            signature = body['signature']
        except KeyError:
            return Response("Bad request data", status=400)

        # from database get corresponding public key
        db_name = 'access'
        client = MongoClient('localhost', 27017)
        db = client[db_name]
        collection = db['id_to_publicKey']
        pubkey_item = collection.find_one({'id': _id})
        if pubkey_item is None:
            return Response("User not registered", status=403)
        
        publicKey = pubkey_item['publicKey']
        if not rsa_verify(signature, _id, publicKey):
            return Response("Authentication error", status=403)

        if isStaleToken(token):
            return Response("Token Expired", status=403)
        
        try:
            decoded = jwt.decode(token, SECRET, algorithm='HS256')
        except DecodeError:
            return Response("Bad request token", status=400)
        decoded['id'].append(childID)
        new_encoded = jwt.encode(decoded, SECRET, algorithm='HS256').decode('ascii')

        if 'expiredTime' in body:
            db_name = 'access'
            client = MongoClient('localhost', 27017)
            db = client[db_name]
            collection = db['token_to_expiration']

            if collection.find_one({'token': new_encoded}) is not None:
                collection.update({'token': new_encoded}, {
                    'token': new_encoded,
                    'expiration': body['expiredTime']
                })
            else:
                collection.insert_one({
                    'token': new_encoded,
                    'expiration': body['expiredTime']
                })
            client.close()

        return new_encoded

    @app.route('/operate', methods=['POST'])
    def operate():
        body = request.get_json()
        try:
            operation = body['operation']
            token = body['token']
            _id = body['id']
            signature = body['signature']
        except KeyError:
            return Response("Bad request data", status=400)

        # from database get corresponding public key
        db_name = 'access'
        client = MongoClient('localhost', 27017)
        db = client[db_name]
        collection = db['id_to_publicKey']
        pubkey_item = collection.find_one({'id': _id})
        if pubkey_item is None:
            return Response("User not registered", status=403)
        
        publicKey = pubkey_item['publicKey']
        if not rsa_verify(signature, _id, publicKey):
            return Response("Authentication error", status=403)
        
        try:
            verifyResult = verify(token, SECRET, operation)
        except DecodeError:
            return Response("Bad request token", status=400)
        if token != "admin" and not verifyResult:
            return Response("Access Denied", status=403)

        operation_url = MASTER_URL + operation['resource']
        headers = {
            'Content-Type': 'application/json',
            'Accept-Charset': 'UTF-8'
        }

        if operation['method'] == 'GET':
            get_url = operation_url + '?' + '&'.join(
                ['{}={}'.format(k, v) for k, v in operation['params'].items()])
            response = requests.get(get_url)

        elif operation['method'] == 'DELETE':
            delete_url = operation_url + '?' + '&'.join(
                ['{}={}'.format(k, v) for k, v in operation['params'].items()])
            response = requests.delete(delete_url)

        elif operation['method'] == 'POST':
            response = requests.post(operation_url,
                                     data=json.dumps(operation['data']),
                                     headers=headers)

        elif operation['method'] == 'PUT':
            response = requests.put(operation_url,
                                    data=json.dumps(operation['data']),
                                    headers=headers)

        if not re.match(r'2..', str(response.status_code)):
            return response

        response = response.json()
        return json.dumps(response)

    app.run(host='0.0.0.0', port=4999)
