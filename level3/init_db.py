from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "level3"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": "http://192.168.1.156:5001/"},
        {"loc": "level4", "url": "http://192.168.1.156:5003/"},
        {"loc": "self", "url": "level3"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "level5", "childLoc": "level4"}
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)