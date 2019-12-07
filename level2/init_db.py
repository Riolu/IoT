from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "level2"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": "http://192.168.1.189:5000/"},
        {"loc": "level3", "url": "http://192.168.1.189:5002/"},
        {"loc": "self", "url": "level2"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "level4", "childLoc": "level3"},
        {"targetLoc": "level4b", "childLoc": "level3"},
        {"targetLoc": "level5", "childLoc": "level3"},
        {"targetLoc": "level5b", "childLoc": "level3"}
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)