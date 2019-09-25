import json
import requests
from eve import Eve
from flask import Flask, redirect, url_for, request

app = Eve()

MASTER_URL = "http://localhost:xxxx"

# urls of all the next-level nodes
next_level_nodes = set()

# which next-level node to find target
find_child = dict()

@app.route("/exp")
def get_exp():
    return "hello world"

locToDbBaseUrl = {
    "columbia": "http://localhost:xxxx"
}

@app.route("/register", methods = ['POST'])
def register():
    if request.data:
        body = json.loads(request.data)
    loc = body["loc"]
    td = body["td"]
    
    
    if loc in next_level_nodes:
        # use Eve to post
        url = locToDbBaseUrl[loc]
        data = td
    elif loc in find_child:
        # go to lower database use register API
        url = locToDbBaseUrl[find_child(loc)] + '/register'
        data = request.data
    else:
        # go to master database use register API
        url = MASTER_URL + '/register'
        data = request.data
        
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    requests.post(url, data=data, headers=headers)


    
    # loc -> master
      
    return request.data
    
if __name__ == '__main__':
    app.run(port=5000)
    