import json
from eve import Eve
from flask import Flask, redirect, url_for, request

app = Eve()

@app.route("/exp")
def get_exp():
    return "hello world"

@app.route("/register", methods = ['POST'])
def register():
    if request.data:
        body = json.loads(request.data)
    return request.data
    
if __name__ == '__main__':
    app.run()
    