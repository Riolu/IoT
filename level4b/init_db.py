from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "level4b"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": "http://192.168.1.189:5002/"},
        {"loc": "level5b", "url": "http://192.168.1.189:5006/"},
        {"loc": "self", "url": "level4b"}
    ]
    CHILD_LOCS = [
    ]

    dbinit(DB_NAME, URLS, CHILD_LOCS)