import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Manhattan']


def register(loc, td):
    '''
    Register a certain td into database.
    input:
    loc: location of the td to be registered
    td: json_ld format
    '''
    







