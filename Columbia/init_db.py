from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "columbia"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": "http://192.168.1.156:5003/"},
        {"loc": "self", "url": "columbia"}
    ]
    CHILD_LOCS = []

    dbinit(DB_NAME, URLS, CHILD_LOCS)