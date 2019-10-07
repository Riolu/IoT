import json
import requests
from eve import Eve
from flask import Flask, redirect, url_for, request

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


@app.route("/exp")
def get_exp():
    return "hello world"

@app.route("/register", methods = ['POST'])
def register():
    if request.data:
        body = json.loads(request.data)
    targetLoc = body["targetLoc"]
    td = body["td"]
    
    if targetLoc in childLoc_to_url:
        # use Eve to post
        url = childLoc_to_url[targetLoc] + '/td'
        data = json.dumps(td)

        # check whether the type is already in type_to_targetLoc
        if td["@type"] not in type_to_targetLoc:
            pass

    elif targetLoc in targetLoc_to_childLoc:
        # go to lower database use register API
        url = childLoc_to_url[targetLoc_to_childLoc(targetLoc)] + '/register'
        data = request.data
    else:
        # go to master database use register API
        url = MASTER_URL + '/register'
        data = request.data
        
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    requests.post(url, data=data, headers=headers)
    
    return data


@app.route("/insertBack", methods = ['GET'])
def insertBack():
    


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
    