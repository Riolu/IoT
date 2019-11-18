import json
import re
from .config import Config
from flask import Flask, request, Response
from pymongo import MongoClient
import jwt
import requests
import datetime
import time;


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

def isSatisfiable(operation_permission, decoded_permission):
    if operation_permission['resource'] != decoded_permission['resource']:
        return False
    for key, value in operation_permission['params'].items():
        if key not in decoded_permission['params'] or (
                value != decoded_permission['params'][key]
                and decoded_permission['params'][key] != '*'):
            return False
    return True

def verify(token, secret, operation):
    decoded = jwt.decode(token, secret, algorithm='HS256')
    decoded_permission = decoded['permission']
    operation_permission = {
        key: operation[key]
        for key in ['resource', 'params']
    }

    db_name = 'access'
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db['token_to_expiration']
    
    token_expiration = collection.find_one({'token': token})
    client.close()
    if token_expiration is not None and token_expiration['expiration'] < time.time():
        return False 

    return isSatisfiable(operation_permission, decoded_permission)


def _requestToken(secret, permission, _id):
    encoded = jwt.encode({
        'id': _id,
        'permission': permission
    },
                         secret,
                         algorithm='HS256')
    return encoded


if __name__ == '__main__':

    app = Flask("access")
    app.config.from_object(Config)
    SECRET = app.config['SECRET']
    MASTER_URL = app.config['MASTER_URL']

    @app.route('/request', methods=['POST'])
    def requestToken():
        body = request.get_json()
        try:
            _id = body['id']
            permission = body['permission']
        except KeyError:
            return Response("Bad request data", status=400)

        return _requestToken(SECRET, permission, _id)

    
    @app.route('/revoke', methods=['POST'])
    def revoke():
        body = request.get_json()
        try:
            token = body['token']
        except KeyError:
            return Response("Bad request data", status=400)
        
        db_name = 'access'
        client = MongoClient('localhost', 27017)
        db = client[db_name]
        collection = db['token_to_expiration']
        
        if collection.find_one({'token': token}) is not None:
            collection.update(
                {'token': token}, 
                {'token': token,
                'expiration': time.time()}
            )
        else:
            collection.insert_one(
                {'token': token, 
                'expiration': time.time()}
            )
        client.close()
        return {}

    # @app.route('/delegate')


    @app.route('/operate', methods=['POST'])
    def operate():
        body = request.get_json()
        try:
            operation = body['operation']
            token = body['token']
        except KeyError:
            return Response("Bad request data", status=400)

        if token != "admin" and not verify(token, SECRET, operation):
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
