import argparse

from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "manhattan"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000"},
        {"loc": "parent", "url": ""},
        {"loc": "columbia", "url": "http://192.168.1.156:5001"},
        {"loc": "self", "url": "manhattan"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "irt", "childLoc": "columbia"},
        {"targetLoc": "cs", "childLoc": "columbia"}
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument('--drop', dest='drop', action='store_true')
    args = parser.parse_args()
    args.set_default(drop=False)

    dbinit(DB_NAME, URLS, CHILD_LOCS, )