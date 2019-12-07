from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "level3"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": "http://192.168.1.156:5001/"},
        {"loc": "level4", "url": "http://192.168.1.156:5003/"},
        {"loc": "level4b", "url": "http://192.168.1.156:5005/"},
        {"loc": "self", "url": "level3"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "level5", "childLoc": "level4"},
        {"targetLoc": "level5b", "childLoc": "level4b"}
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)