from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "level1"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": ""},
        {"loc": "level2", "url": "http://192.168.1.156:5001/"},
        {"loc": "self", "url": "level1"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "level3", "childLoc": "level2"},
        {"targetLoc": "level4", "childLoc": "level2"},
        {"targetLoc": "level5", "childLoc": "level2"}
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)