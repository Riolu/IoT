from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "level4"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": "http://192.168.1.189:5002/"},
        {"loc": "level5", "url": "http://192.168.1.189:5004/"},
        {"loc": "self", "url": "level4"}
    ]
    CHILD_LOCS = [
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)