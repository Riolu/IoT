import json
import requests
from eve import Eve
from flask import Flask, redirect, url_for, request
from pymongo import MongoClient

app = Eve()

def retrieve(key, field, baseUrl, tableName):
    url = baseUrl + tableName + '/' + key
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
            requests.put(host_url+"info", data=json.dumps(info_data), headers=headers)

    elif child_loc is not None:
        # go to lower database use register API
        child_url = retrieve(child_loc, "url", host_url, "loc_to_url")
        url = child_url + '/register'
        data = request.data
    else:
        # go to master database use register API
        master_url = retrieve("master", "url", host_url, "loc_to_url")
        url = master_url + '/register'
        data = request.data
        
    requests.post(url, data=data, headers=headers)
    
    return data


@app.route("/info", methods = ['PUT'])
def info():
    if request.data:
        body = json.loads(request.data)
    type = body["type"]
    targetLoc = body["targetLoc"]

    # add to type_to_targetLoc
    client = MongoClient('localhost', 27017)
    db = client['manhattan']
    collection = db['type_to_targetLocs']

    collection.update(
        {'type': type}, 
        {'$push': {'targetLocs': targetLoc}}
    )
    client.close()

    host_url = request.host_url
    url = host_url + 'loc_to_url/parent'
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        parent_url = response.json().get('url', None)
        if parent_url:
            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
            requests.put(parent_url + '/info', data=request.data, headers=headers)
    
    return {}

    
if __name__ == '__main__':
    app.run(port=5000)
    