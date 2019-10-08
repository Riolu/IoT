import json
import requests
from eve import Eve
from flask import Flask, redirect, url_for, request
from pymongo import MongoClient

app = Eve()

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

MASTER_URL = "http://localhost:5000"
PARENT_URL = "http://localhost:5001"

# urls of all the next-level nodes
childLoc_to_url = {
    "columbia": "http://localhost:5001"
}

# which next-level node to find target by location
targetLoc_to_childLoc = dict()

# type -> list of loc nodes
type_to_targetLoc = dict()

def retrieve(key, field, baseUrl, tableName):
    url = '/'.join([baseUrl, tableName, key])
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get(field, None)
    else:
        return None

@app.route('/register', methods = ['POST'])
def register():
    if request.data:
        body = json.loads(request.data)
    targetLoc = body['targetLoc']
    td = body["td"]

    host_url = request.host_url
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    
    child_url = retrieve(targetLoc, "url", host_url, "loc_to_url")
    child_loc = retrieve(targetLoc, "targetLoc", host_url, "targetLoc_to_childLoc")
    
    if child_url is not None:
        # use Eve to post
        url = child_url + '/td'
        data = json.dumps(td)

        # check whether the type is already in type_to_targetLoc
        
        type_locs = retrieve(td["@type"], "targetLocs", host_url, "type_to_targetLoc")
        if type_locs is None:
            info_data = {
                "type": td["@type"],
                "targetLoc": targetLoc
            }
            requests.post(host_url+"info", data=info_data, headers=headers)

    elif child_loc is not None:
        # go to lower database use register API
        child_url = retrieve(child_loc, "url", host_url, "loc_to_url")
        url = child_url + '/register'
        data = request.data
    else:
        # go to master database use register API
        url = MASTER_URL + '/register'
        data = request.data
        
    requests.post(url, data=data, headers=headers)
    
    return data


@app.route("/info", methods = ['POST'])
def info():
    if request.data:
        body = json.loads(request.data)
    type = body["type"]
    targetLoc = body["targetLoc"]

    # add to type_to_targetLoc
    client = MongoClient('localhost', 27017)
    db = client['manhattan']
    collection = db['loc_to_url']

    collection.update(
        {'type': type}, 
        {'$push': {'targetLocs': targetLoc}}
    )
    client.close()

    host_url = request.host_url
    url = host_url + 'loc_to_url/parent'
    response = requests.get(url)
    if response.status_code == 200:
        parent_url = response.json().get('url', None)
        headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
        requests.post(parent_url + '/info', data=request.data, headers=headers)



    
    


# @app.route("/queryByLoc", methods = ['GET'])
# def query():
#     if request.data:
#         body = json.loads(request.data)
#     loc = body["loc"]
#     td = body["td"]
    
#     if loc in next_level_nodes:
#         # use Eve to post
#         url = next_level_nodes[loc] + '/td'
#         data = json.dumps(td)
#     elif loc in find_child:
#         # go to lower database use register API
#         url = next_level_nodes[find_child(loc)] + '/register'
#         data = request.data
#     else:
#         # go to master database use register API
#         url = MASTER_URL + '/register'
#         data = request.data
        
#     headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
#     requests.post(url, data=data, headers=headers)
    
#     return data
    
if __name__ == '__main__':
    app.run(port=5000)
    