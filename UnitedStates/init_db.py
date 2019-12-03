from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "united_states"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": ""},
        {"loc": "new_york_state", "url": "http://192.168.1.156:5000/"},
        {"loc": "self", "url": "united_states"}
    ]
    CHILD_LOCS = [
        {"targetLoc": "new_york", "childLoc": "new_york_state"},
        {"targetLoc": "manhattan", "childLoc": "new_york_state"},
        {"targetLoc": "columbia", "childLoc": "new_york_state"},
        {"targetLoc": "mta", "childLoc": "new_york_state"}
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)