from .config import Config
from flask import Flask, request, Response
import jwt
import requests

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

if __name__ == '__main__':
    def isSatisfiable(operation_permission, decoded_permission):
        if operation_permission['resource'] != decoded_permission['resource']:
            return False
        for key, value in operation_permission['params']:
            if key not in decoded_permission or (value != decoded_permission[key] and decoded_permission[key] != '*'):
                return False
        return True

    def verify(token, secret, operation):
        decoded = jwt.decode(token, secret, algorithm='HS256')
        decoded_permission = decoded['permission']
        operation_permission = {key: operation[key] for key in ['resource', 'params']}
        return isSatisfiable(operation_permission, decoded_permission)

    app = Flask()
    app.config.from_object(Config)
    SECRET = app.config['SECRET']

    def requestToken(secret, permission, _id):
        encoded = jwt.encode({'id': _id, 'permission': permission}, secret, algorithm='HS256')
        return encoded

    @app.route('/request', methods = ['POST'])
    def request():
        body = request.get_json()
        try:
            _id = body['id']
            permission = body['permission']
        except KeyError:
            return Response("Bad request data", status=400)

        return requestToken(SECRET, permission, _id)


    @app.route('/revoke')

    @app.route('/delegate')

    @app.route('/operate', methods = ['POST'])
    def operate():
        body = request.get_json()
        try:
            operation = body['operation']
            token = body['token']
        except KeyError:
            return Response("Bad request data", status=400)

        if not verify(token, SECRET, operation):
            return Response("Access Denied", status=403) 

        master_url = ?
        
        if operation['method'] == 'GET':
            get_url = master_url + operation['resource'] + '?' # can extract a function if needed
            for key, value in operation['params']:
                get_url += key + '=' value + '&'
            if get_url[-1] == '?' or get_url[-1] == '&':
                get_url = get_url[:-1] 

            response = requests.get(get_url)
            if not re.match(r'2..', str(response.status_code)):
                return response
            response = response.json()
            return json.dumps(response)

        else if operation['method'] == 'POST':
            post_url = master_url + operation['resource']
            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
            requests.post(post_url, data=json.dumps(operation['data']), headers=headers)


        else if operation['method'] == 'DELETE':

        else if operation['method'] == 'PUT':
        
        
    app.run(host='0.0.0.0', port=4999)
