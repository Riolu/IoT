from .run import _requestToken
from .config import Config
import jwt

def main():
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
                'loc': 'columbia',
                'type': 'tv'
            }
        }
    }, {
        'id': ['z'],
        'permission': {
            'resource': 'delete',
            'params': {
                'targetLoc': 'columbia',
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