from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode, b64decode
import json


def sign(msg, privateKey):
    # keyDER = b64decode(privateKey)
    keyPriv = RSA.importKey(privateKey)

    hashObj = SHA.new(msg.encode("utf-8"))
    signer = PKCS1_v1_5.new(keyPriv)

    sig = signer.sign(hashObj)
    res = b64encode(sig)

    return res


if __name__ == '__main__':
    privKey = {
        'alita':
        '-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAnnlzTo6qzhD4UHTAH+KYK6ZI/7uqIqMDlQE+ioLMWXUoy4XH\ne7NTruU8yTXgOHo1h/ObJ/quM6xIPBJlYevmnhkwsSuy2gifcYki9FmoyVcIJOR9\nIPEhivfwCCmTte4PRR4JGNvdqE5UJWSraqT37AtdDDlBTeePtF6gIQppdW02Ju4c\nV5N2+OjFryLyUtOHOA0Q2vW7lrbPzhUxaNUczqcDE+8BxtN5/kst8HcyKLRoMlrA\n+4L3s6SEEPQ4ku6qs9maKnC5dUhvuJIXTKEjqNPzfCOpK6D5mWZ5K2b70DzGP+3U\nWW3UWe4n8iWV99baUNnVKU4e8WXiF4YcUPDgEQIDAQABAoIBAFzeg4o35TTZkQtl\nP+nvmomJ6yGi0nN14HWDwyjcufB6zitm/J4rWxEVWef4YKv4QkKnqfdl2oyBm9tI\nVI1r9zwTOwu4thk8EGQyn39ew6EqFaW5GPMjHCsaXVoLM3rcRaqVjXM59c3aCUnY\nkvPuNTPo/OBa9UA4QWjMQz7ZoS+kolNsUhVF4ch2gj0B+t/8xDzqNvFFejAufesU\nQeHmuBAmYS+Iq351iPuzLWJyd98fKDqvN8YS/KI9rgypuCb47DUgcCUDU4Vv1yM2\nVhuS/SlWNXKb/jNisrOCEnxIVDyGhsUQd027U+vqwbD0BwZf4yj681/iFRj2YndO\nSCq/LKECgYEAwG3Z2hCZelJcrDAwwZc0c2z9g70yCgxcyMMwtcilq8wjuKEAYg+H\n0hg6sNmsXGiIIvitfoukIjfLS39gfpUh41UXLYNFooMNbzdrWYeKntFeEM86Ty68\nGfXQ2WK6Pw7ZIiXShfFclaCaMlgKKMUwu7oQUh4bbBayZNNHLIRnlD0CgYEA0tP6\nL67QWKyEiT3chyII0b0uDdijm9pO14hnsi0XtklaJ65/QtfNuCC/XFmYoJoJ6CJd\nNzQWil4JqjBJgYrS9OVjMNpIqwm5ce7e+9PTNFvUpu7CICXQotxG8XLh+pfpHkJK\nyiwqdOumH1t9/BDxARTHskwmyYzqrzvy5hZDNGUCgYA76DchZ3eQmGGXja0wJ9XB\ndZX7VIRmknC0Y+gfP+cr8/LPAPiwjqs3IinrcujxH+36DTdeJTUlHf+hcndlESKq\ntovvtGWScYBWNoeqKMNkLEQ/sXQywJb48gliFBVtmj7JHcNLxdeQEZ7Pu472IGXK\nm+OG3S6mWO6S6x/GYTYp9QKBgQCU2pYKlKMF+MibHdJWlvEjJS8fF5Zss/Z2txh/\n9NaJHcFJwyqXR0c4eeaijZ/1xMy52Yl3MI+5oiuwvecoT5wizNL76yLjoDoO91j4\n9NZqYWwDcRAfIpPsaRqt3y8uf5NYifXESOqxIrBn83FAR7XhzYoxmRLJu3T3xJv7\nWDybAQKBgALxrooXAVi0tjsADc0W510nD8Tq27w32mAWjrpCjS+T/5LQwE/qSdqv\nmEU6G+dNCdIPx2tC0QN+y9hES8uJwOsWyLzsUx7eegnr8yUIfVmy9skBX9KowMkP\npxnt6hyEJtYyAYQJI+WowYtLmnT0BV5pSACIx7At3XsNz52ifBVS\n-----END RSA PRIVATE KEY-----',
        'brian':
        '-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAwxyl4H99t6S0h8xPqunqX9RgKKsXTHzjeZ6T4Tf+xebbAXUv\neM3Ed3YFF2yHUF/H52m4ucG/CWbS4JieT750oyIwGfEcWzklokXscdR2asPdEpLK\nQ/LHlt4sGAFS5ev8RBELT7M/rcVVU/YA9lgPhbsyTPVJ7TuedioLz78TTSEV2sEy\nh3Qae8iDUyevUdnGZBzR8/vFMosnkxYGGLLfOT9nFED3gcaal9gms2qSv92L4uDC\nQYHAxWxOs3UPDI9fLZPWErFhGKek1GQ4DGLvKp491OR63QdhpgFibdAn5WppglB8\nzMwZTyHuxXN4dBgfsukUP/PlefMw61RjbJbAywIDAQABAoIBAA8Mo6LIUqsaki4z\nTSXSuxg/KleYsshcjbMwzxk9F3KuVtAq+MlpnbDVMplW7qz9Zk7sMapqTlDsVHGs\nc/GUsCxxE6K8nUJQCx4UJKO3Dpc3mlK3bdCF5m01n9MOLxW6+Q9K/UNdgRjnMqiy\nPerCahgXk06qUNRyl8tnfNe+Vj/JneNhsA3WlV4jkhDVLDPYOIISHvTwjEa+ePUq\nrpGubaCMFxlEukMjjEgkgj6rWb16u92mWcjiySAUeqn+GeSBu+eNVspBnLjuQxiv\n6CWypofvX39x+R6AV3KMfbAWb7iBidgS/Llvgl83rEKZjtxWYBaHyCAC9HOP4BnE\nPhDExZECgYEAy1vy/xVpJwSreWxNAb7+GTs/OSVzh6KzwE/yZiWTNlvobmTPok2+\nUhAxmj25Yc1joBJFaBApvLmv1ZgT6eIPViMUSLoy224t2u+i1tw8RGSbBX0UPiJ1\nuOrQC6DK8I7mSsiqmn++9xQ32qMy3nj/FZfKXytX36ku0sFLKql/lbkCgYEA9Z4s\nx6aT7gKJWoFAntXwRSzIrhLf5HdXzF0jIbqoLWX9GSEYH64xVVu0AASTi1p5CvDa\n/Qxlb4RWSeJEIfHZgCOA5vQZfZYRQqD+t3P439FPkVT0HU5fUpfY2phYbqSYKCoV\ndedZNYn3OLwdYZ7ddju9l3cBLxA0wvY1/6LjzKMCgYBYNHe/oH/Nhr8BmbIFEdyR\nARu5I79qk223+nU/TQj/SPoV9+//jA0C9zcsmZ0xCK8vnP0x1+DilP/pe18X0Q+p\n4ulHakvo1W9aSRquazRQzfpXdRs0oCnDnUXD5Whg0vqccVFeVg50iPZ5BNRpnr21\nlfMXOGuS/YTrsR9zT7WhMQKBgGQeN66iLgaErixgJ1EXb7siyCJ8uxrLstQw2tMy\n3L60pfiKTuULAj0DBlpDg0j4dgKJrxoa5XYRgYLYYmFbzga3ciGyOnnApAR+z5VE\nBpxlG4PoFyGjAqQOFWz1UIa5PPSSQvEufmSeelF8DJXwReGd9Gg7MBZZCsi1x8kO\nQsD1AoGAV1eWB+FsMGV2kSBLKSVGlj0FcHl/CgZ66Z/dNppypjYvpy/CZRu076jL\nsB97Qg9JeHy1H6TEe7mzJSynjKEuBp1LXmLU9/YKNtz0nsifBX0UqWCrrC4hjVbU\nn8Yx+iD+kp1K/A/KojDzQPmnBCSkX6qbSXmucm5/VpmV0Qsks10=\n-----END RSA PRIVATE KEY-----'
    }

    alita_operations = [{
        'resource': 'register',
        'method': 'POST',
        'params': {},
        'data': {
            "td": {
                "_type": "tv",
                "id": "urn:dev:ops:23112-tv-1",
                "publicity": 1
            },
            "targetLoc": "level5"
        }
    }, {
        'resource': 'register',
        'method': 'POST',
        'params': {},
        'data': {
            "td": {
                "_type": "pc",
                "id": "urn:dev:ops:23221-pc-10"
            },
            "targetLoc": "level5"
        }
    }, {
        'resource': 'searchByLocType',
        'method': 'GET',
        'params': {
            'loc': 'level5',
            'type': 'tv'
        }
    }, {
        'resource': 'searchPublic',
        'method': 'GET',
        'params': {
            'loc': 'level4'
        }
    }, {
        'resource': 'searchPublic',
        'method': 'GET',
        'params': {
            'loc': 'level4b'
        }
    }, {
        'resource': 'searchByLocId',
        'method': 'GET',
        'params': {
            'loc': 'level5',
            'id': 'urn:dev:ops:23112-tv-1'
        }
    }, {
        'resource': 'relocate',
        'method': 'PUT',
        'params': {
            'fromLoc': 'level5',
            'toLoc': 'level5b',
            'id': 'urn:dev:ops:23112-tv-1'
        },
        'data': {}
    }, {
        'resource': 'delete',
        'method': 'DELETE',
        'params': {
            'targetLoc': 'level5b',
            'id': 'urn:dev:ops:23112-tv-1'
        }
    }]

    print('alita')
    print('delegate')
    print(sign('brian', privKey['alita']))
    print('revoke')
    print(
        sign(
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSIsImJyaWFuIl0sInBlcm1pc3Npb24iOnsicmVzb3VyY2UiOiJzZWFyY2hCeUxvY1R5cGUiLCJwYXJhbXMiOnsibG9jIjoiKiIsInR5cGUiOiIqIn19fQ.lJqQJgK_dwrWgbI660OvyAuQ0LaV6IG2QS3mp4P1L5s',
            privKey['alita']))

    for operation in alita_operations:
        print(operation['resource'])
        print(sign(json.dumps(operation), privKey['alita']))

    brian_operations = [{
        'resource': 'searchByLocType',
        'method': 'GET',
        'params': {
            'loc': 'level5',
            'type': 'pc'
        }
    }]

    print('brian')
    for operation in brian_operations:
        print(operation['resource'])
        print(sign(json.dumps(operation), privKey['brian']))