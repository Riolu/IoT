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

def getSelfName(baseUrl):
    return retrieve('self', 'url', baseUrl, 'loc_to_url')

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

        info_data = {
            "type": td["_type"],
            "targetLoc": targetLoc
        }
        requests.put(child_url+"/info", data=json.dumps(info_data), headers=headers)

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

    # check whether the type is already in type_to_targetLoc
    type_locs = retrieve(type, "targetLocs", request.host_url, "type_to_targetLocs")
    if type_locs is not None:
        return {}
    
    # add to type_to_targetLoc
    client = MongoClient('localhost', 27017)
    db_name = getSelfName(request.host_url)
    db = client[db_name]
    collection = db['type_to_targetLocs']

    
    if collection.find_one({'type': type}) is not None:
        collection.update(
            {'type': type}, 
            {'$push': {'targetLocs': targetLoc}}
        )
    else:
        collection.insert_one(
            {'type': type, 
             'targetLocs': [targetLoc]}
        )
    client.close()

    host_url = request.host_url
    url = host_url + 'loc_to_url/parent'
    response = requests.get(url)

    if response.status_code == 200:
        parent_url = response.json().get('url', None)
        if parent_url:
            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
            requests.put(parent_url + '/info', data=request.data, headers=headers)
    
    return {}

# search by type at a certain loc
@app.route("/searchAtLoc", methods = ['GET'])
def searchAtLoc():
    type = request.args.get("type")
    print(type)

    type_locs = retrieve(type, "targetLocs", request.host_url, "type_to_targetLocs")

    if len(type_locs) == 0:
        # use Eve to get
        url = request.host_url + '/td/' + type
        return requests.get(url)

    child_url_set = set()
    for target_loc in type_locs:
        target_url = retrieve(target_loc, "url", request.host_url, "loc_to_url")
        if target_url:
            child_url_set.add(target_url)
        else:
            child_loc = retrieve(target_loc, "targetLoc", request.host_url, "targetLoc_to_childLoc")
            child_url = retrieve(child_loc, "url", request.host_url, "loc_to_url")
            child_url_set.add(child_url)
    
    result_list = list()
    for child_url in child_url_set:
        result_list.append(json.loads(requests.get(
            child_url+'/searchAtLoc?type='+type
            )))
    
    return json.dumps(result_list)


@app.route("/searchByLocType", methods = ['GET'])
def searchByLocType():
    loc = request.args.get('loc')
    type = request.args.get('type')

    host_url = request.host_url
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    
    self_loc = getSelfName(host_url)
    child_url = retrieve(targetLoc, "url", host_url, "loc_to_url")
    child_loc = retrieve(targetLoc, "targetLoc", host_url, "targetLoc_to_childLoc")

    if self_loc == loc or target_url is not None:
        target_url = host_url if self_loc==loc else target_url
        response = requests.get(
            target_url + 'searchAtLoc',
            params={
                'type': type
            },
            headers=headers
        )
    else:
        target_url = retrieve(
            child_loc if child_loc is not None else 'master',
            "url",
            host_url,
            "loc_to_url"
        )
        response = requests.get(
            target_url + 'searchByLocType',
            params={
                'loc': loc,
                'type': type
            },
            headers=headers
        )

    return response.data


    
if __name__ == '__main__':
    app.run(port=5000)
    