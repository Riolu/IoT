from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "manhattan"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": ""},
        {"loc": "columbia", "url": "http://192.168.1.156:5001/"},
        {"loc": "self", "url": "manhattan"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "irt", "childLoc": "columbia"},
        {"targetLoc": "cs", "childLoc": "columbia"}
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)