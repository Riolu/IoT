import argparse
from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "columbia"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000"},
        {"loc": "parent", "url": "http://192.168.1.189:5000"},
        {"loc": "self", "url": "columbia"},
        {"loc": "irt", "url": "http://192.168.1.156:5002"},
        {"loc": "cs", "url": "http://192.168.1.156:5003"}
    ]
    CHILD_LOCS = []

    parser = argparse.ArgumentParser()
    parser.add_argument('--drop', dest='drop', action='store_true')
    parser.set_default(drop=False)
    args = parser.parse_args()

    dbinit(DB_NAME, URLS, CHILD_LOCS, args.drop)