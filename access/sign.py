from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode, b64decode

def sign(_id, privateKey):
    # keyDER = b64decode(privateKey)
    keyPriv = RSA.importKey(privateKey)

    hashObj = SHA.new(_id.encode("utf-8"))
    signer = PKCS1_v1_5.new(keyPriv)

    sig = signer.sign(hashObj)
    res = b64encode(sig)

    return res


if __name__ == '__main__':
    ls = [
        ('a','-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA1Wn/NFUj+K5X+GCzNoqgl0K4ZPeSNKaMC7BULn4Mu3p+XawJ\nyL2i/ahjQzauJQiqjju/U0FwteudNcwzuXmoh7IXWgdl9QE4iJMsTpOnJvz9IGgW\n0T2O/PHmhqgDKH/4O/DXIvXW8D/vCOYtNXqyuZrYSee5Geo4rwVHpkzijz5H7pGi\nMYrB8HJzl4046DRBiNDmjZDQSwVsalAGAtzgZvNLHqIlybsH4rVKRGzrg3CfnDJi\naoqwxaySqij2+5PwmQ/3TlTlLyTiSNRkmA42z/slNJheKYUOJhTbIugiYQOweq2l\nHyiKDq/lDH5gG81A3hUuLSod9tq/VvP2szqaYQIDAQABAoIBAFFoEHA+9ey7XFUj\nVdk9QgrQ6ZOiGEQ7L3qZ9VKSxHqTPDaxFD5dkBngLJUL+5um1aBRzCaO9NaAHMTT\nsvtSG+Y/Gcc+wTaXE6CNOz5x9jXaFRhSfDmumKeGAqBk4GeHgQIkWXw9eJLGYIDt\nhFs9BYXlOhHe8W2gOaURh4Y5F8b5kU7qvXKwPF8B12JpaiuscsQyuRmTzdVB/gL+\nAXGDMime80zOu0qj3cxTSrwPYY2Gv6tgbZh/ONc+Kk8vFb9+Y+/c5XGcUTtYoQiY\n0yApsQbNXqIN9/FbBlIQy9hordW3rh0YnGHj5TmVLIHpcKtKbFjlxo6aycuREtRp\nBTQq7p0CgYEA3QUMNrKuD1BMvXtpzQt5lGWfyeFaIBryClutrl435iz9BNyMr9Dg\nOHYcyEKwHiw+YLUJYWA60ZWDbfuBW2yKCG5BFpq7/MVFU22v/pQsEoygMzDQZktK\nNDthbChxcPYEceZIU3OckvclznjGN46VxwRH6+t1IDGuI9wRIw/9KWcCgYEA9zDL\nPtpswlzTHlLv1Z0w/VAxhMDO3ePeTeI7R0YOtodouNnOL8KRljrD1ZsbYFJ47ErU\nPpX+OLm69giaOWDFZ4ZMMl0WuSB2EVOnHCQXYS2hnCejCpWQdEJjanXTEbw1XeML\ngXeawuwi74TsKdrbyXy3GAqzxMIafO2MqFl6GPcCgYA79yOiL4ZkJ0A65KIG/McG\nyS+6QUcHkOf8gXU06uE1tR0M1Z3iEcTT7M/QUa+g8BYYfOXHoqkyteML0wH8wQ0O\nToOgU2kPoqI1iXwHkUIH4lmQqfzQ1DqUw0uiYbKtmEIKeRVEdwiTIzUBuOjmp+vh\nLDsrOh30FyaNGicYIT1pnwKBgQDNUAfgosenADaSf0yZXsCsBgm7O/IWtweUJQ4b\newMJdJr0vmPVo4QNBa5XI0evz5CEovp7KVZIg2vYoviGI+ySuidbxZn0FhQ6/AJX\nC1sn6iDLdNilF+ktx16PtGGl329sFgMee9tdf4jc7MjDUvcu+ZmSLIF4MciSbzRf\nOEKDrQKBgBjBrp9Mf67Eh4ztsekhljf4qmmYkMjEAJ1o8DQrMw+AiPGFLeRHTyJo\nM15YcmDg1HDp5YzqnhFERWHoPEEjlrK2b4AMQsHmq0nQoBxCmLhfPFf8hjh7GOnX\nCdVvWz2YvpIs90DMw1jHgJ36qZWrLeQTzlcKNQNCNxmqbwVnTNWp\n-----END RSA PRIVATE KEY-----'),
        ('b',"-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEA6cDLMzVsdgAbVcLATf6cVc3JpX1VtOYVANrrghvlDF6RINHy\nOIrai8qEP1wePVTsaS5xVG5WOnt27kEhDNUp5tUZn0Vpi9Rq5Op+qz3nyn6j7DfO\nWk/ntkX/suNTtDd080X5U4fEGuObntg/hSLu6LVQ2uU4zuOb3rEQRqUkFc7+Wk49\n3eOxqQo8+5u/efqjeTYyf64UP2IWb1zAT2HfWvDTr8KVIo/9EYCNupYUZ8AotPqq\nG3/v1AgDZIph4yJZh+4BVskg4pq9wsc3lvhlak39+Aih7KbrKhGBzEkDYILa94o4\nPQblNC/gFTUW7tVzsfC36lcZv6ngxEgp6Qq5kwIDAQABAoIBAQCzNP+ULu0MOmC6\niyhrozuv/KkPmttOaObJVQ0hHsmnhgi1pL+S4cFTUtu4x6LXWng020o/dKffBjDT\n0FLKR9JsCgwus0SL0zpwbebW2gsOj7CUtOQbEQ+QCnJSbz4I+EtNBuRzSa7q/nyc\ndyWbqICJIBjw+LNoyc8CF7Vms8zKegQBEhkpghLbRymmndfliy4+LcYCpr7GvMcZ\nLIk2NFlmVLPZcTosDxyrcIoxN9ZJMElqWcj/qAS20M2YD7ZYE5mx9pryD+Doj2+u\nJ8mqsvyc2GP8KYlVLpqrEY9DD/Z4Qd53uBnCnRcIT05Q7rg6bD/LGmN9Jlm3b62D\nKMiusAEBAoGBAO29B6fO8El/Xas43tMkC2PtKGQi1IXcq/O7vDoZfAuSMZZHEF2j\nFHhV+Tfexux1F76SQEbkCOmOOBME3sGoRUvTF1+ThRIVLOqifHvrS8O69DGIewbn\n6Ao0TwrE8J+8P1nqZmxzyCM4HGWfXzapJVHlzAJxiJaTHPtSPkYjHsozAoGBAPu1\nZUSUORtCltbH0LhjiHhhqY2hxeG2zcm7DCRJ16T6DqbY0w1DUAXPVRbK0mYqGafv\nuDsE1aEMabVEBxoWFksgGYQlfFVwbkrQHhnBQQacOo0MqLQ8XUwnM6BRBl6/y8uY\nYxHxR0S3/j+ztJvuMSErP46mOb1+eRoYJhOri7MhAoGAK+/Til/kaLDxTsOj6sGu\nmTkrTdZiEJtH7DO2BcbP9hN+tpdLnwKUteittnWlre22BbJhzrg2LXPrSRiNUp0W\nsXzBxRgub7kaJAMDnqNNzU6v8reWhSA28ivYr9TV46+WxbdcVo7PXjLwjJd3sVJx\nY0FlAs6Yv7tQj+ITQEMdXaECgYEAnANyElDBGKlsbxIIx9FBrEP0YQotadrxsKEU\nRIXUeLhZTodEQYtAVWmONwNd598ead4G1eYIN7tG5giVUlDwXn418pd9ekOmyQ44\nKgSDtoItNHHtO1HTDjmaITs3dJDy023PsjZX0zssBvXu81tu7j0tNtDHJzH2A/uF\n1llUzKECgYEA5ygTCkoFPdXAgGIk8Vl81/kb6Y1AmlgMrukawNaGqF2k5AGn2FNg\n6PgDyZvMIhue7v7BvhWzRMuaWpvBxQ+cvTCqh6Y5TldarLLubmyM7nIgS43GJ9FK\ng+MNnNxnWERgmaYgz1uIYLWQp5y+uCoW0ppvLsh/FnPtrHqviP6C8UA=\n-----END RSA PRIVATE KEY-----")
    ]
    for (_id, key) in ls:
        res = sign(_id, key)
        print(res)