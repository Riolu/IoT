from ..run import _requestToken
from ..config import Config
import jwt


def getTokens():
    SECRET = Config.SECRET

    permissionRequestList = [{
        'id': ['alita'],
        'permission': {
            'resource': 'register',
            'params': {}
        }
    }, {
        'id': ['alita'],
        'permission': {
            'resource': 'searchByLocType',
            'params': {
                'loc': '*',
                'type': '*'
            }
        }
    }, {
        'id': ['alita'],
        'permission': {
            'resource': 'searchPublic',
            'params': {
                'loc': '*'
            }
        }
    }, {
        'id': ['alita'],
        'permission': {
            'resource': 'searchByLocId',
            'params': {
                'loc': '*',
                'id': '*'
            }
        }
    }, {
        'id': ['alita'],
        'permission': {
            'resource': 'relocate',
            'params': {
                'fromLoc': '*',
                'toLoc': '*',
                'id': '*'
            }
        }
    }, {
        'id': ['alita'],
        'permission': {
            'resource': 'delete',
            'params': {
                'targetLoc': '*',
                'id': '*'
            }
        }
    }]

    # tokens = [
    #     _requestToken(SECRET, item['permission'], item['id']) for permissionRequest in permissionRequestList
    # ]

    # for token in tokens:
    #     print(jwt.decode(token, SECRET, 'HS256'))

    for permissionRequest in permissionRequestList:
        print(permissionRequest['permission']['resource'])
        print(_requestToken(SECRET, permissionRequest['permission'], permissionRequest['id']))


if __name__ == '__main__':
    getTokens()