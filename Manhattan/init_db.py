from ..src.dbinit import dbinit

if __name__ == '__main__':
    DB_NAME = "manhattan"
    URLS = [
        {"loc": "master", "url": "http://192.168.1.189:5000/"},
        {"loc": "parent", "url": "http://192.168.1.189:5002/"},
        {"loc": "self", "url": "manhattan"},
        {"loc": "mta", "url": "http://192.168.1.189:5005/"},
        {"loc": "columbia", "url": "http://192.168.1.189:5004/"}
    ]
    CHILD_LOCS = []

    dbinit(DB_NAME, URLS, CHILD_LOCS)