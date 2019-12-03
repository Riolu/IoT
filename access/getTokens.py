from .run import _requestToken
from .config import Config
import jwt

def main():
    SECRET = Config.SECRET

    data = [{
        'id': ['a'],
        'permission': {
            'resource': 'register',
            'params': {}
        }
    }, {
        'id': ['a'],
        'permission': {
            'resource': 'searchByLocType',
            'params': {
                'loc': '*',
                'type': '*'
            }
        }
    }, {
        'id': ['a'],
        'permission': {
            'resource': 'searchByLocTypeIterative',
            'params': {
                'loc': '*',
                'type': '*'
            }
        }
    }, {
        'id': ['a'],
        'permission': {
            'resource': 'searchPublic',
            'params': {
                'loc': '*'
            }
        }
    }, {
        'id': ['a'],
        'permission': {
            'resource': 'relocate',
            'params': {
                'fromLoc': '*',
                'toLoc': '*',
                'id': '*'
            }
        }
    }, {
        'id': ['a'],
        'permission': {
            'resource': 'delete',
            'params': {
                'targetLoc': '*',
                'id': '*'
            }
        }
    }]

    tokens = [
        _requestToken(SECRET, item['permission'], item['id']) for item in data
    ]

    print(tokens)

    for token in tokens:
        print(jwt.decode(token, SECRET, 'HS256'))

    return tokens

if __name__ == '__main__':
    main()



#   data = [{
#         'id': ['x'],
#         'permission': {
#             'resource': 'register',
#             'params': {}
#         }
#     }, {
#         'id': ['y'],
#         'permission': {
#             'resource': 'searchByLocType',
#             'params': {
#                 'loc': 'columbia',
#                 'type': 'tv'
#             }
#         }
#     }, {
#         'id': ['z'],
#         'permission': {
#             'resource': 'delete',
#             'params': {
#                 'targetLoc': 'columbia',
#                 'id': '*'
#             }
#         }
#     }]