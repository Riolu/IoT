from run import app
from flask import jsonify

@app.route("/exp")
def get_exp():
    return "hello world"