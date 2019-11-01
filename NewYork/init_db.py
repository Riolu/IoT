from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "new_york"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": ""},
        {"loc": "manhattan", "url": "http://192.168.1.156:5001/"},
        {"loc": "self", "url": "new_york"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "columbia", "childLoc": "manhattan"},
        {"targetLoc": "mta", "childLoc": "manhattan"}
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)