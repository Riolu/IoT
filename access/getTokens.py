from .run import _requestToken
from .config import Config

if __name__ == '__main__':
    SECRET = Config.SECRET

    data = [{
        'id': ['x'],
        'permission': {
            'resource': 'register',
            'params': {}
        }
    }, {
        'id': ['y'],
        'permission': {
            'resource': 'searchByLocType',
            'params': {
                'loc': 'NewYork',
                'type': 'tv'
            }
        }
    }, {
        'id': ['z'],
        'permission': {
            'resource': 'delete',
            'params': {
                'targetLoc': 'NewYork',
                'id': '*'
            }
        }
    }]

    tokens = [
        _requestToken(SECRET, item['permission'], item['id']) for item in data
    ]

    return tokens