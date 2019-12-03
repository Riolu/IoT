from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "new_york_state"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": "http://192.168.1.189:5000/"},
        {"loc": "self", "url": "new_york_state"},
        {"loc": "new_york", "url": "http://192.168.1.189:5001/"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "manhattan", "childLoc": "new_york"},
        {"targetLoc": "columbia", "childLoc": "new_york"},
        {"targetLoc": "mta", "childLoc": "new_york"}
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)