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
    ls = [(
        'x',
        '-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA1Wn/NFUj+K5X+GCzNoqgl0K4ZPeSNKaMC7BULn4Mu3p+XawJ\nyL2i/ahjQzauJQiqjju/U0FwteudNcwzuXmoh7IXWgdl9QE4iJMsTpOnJvz9IGgW\n0T2O/PHmhqgDKH/4O/DXIvXW8D/vCOYtNXqyuZrYSee5Geo4rwVHpkzijz5H7pGi\nMYrB8HJzl4046DRBiNDmjZDQSwVsalAGAtzgZvNLHqIlybsH4rVKRGzrg3CfnDJi\naoqwxaySqij2+5PwmQ/3TlTlLyTiSNRkmA42z/slNJheKYUOJhTbIugiYQOweq2l\nHyiKDq/lDH5gG81A3hUuLSod9tq/VvP2szqaYQIDAQABAoIBAFFoEHA+9ey7XFUj\nVdk9QgrQ6ZOiGEQ7L3qZ9VKSxHqTPDaxFD5dkBngLJUL+5um1aBRzCaO9NaAHMTT\nsvtSG+Y/Gcc+wTaXE6CNOz5x9jXaFRhSfDmumKeGAqBk4GeHgQIkWXw9eJLGYIDt\nhFs9BYXlOhHe8W2gOaURh4Y5F8b5kU7qvXKwPF8B12JpaiuscsQyuRmTzdVB/gL+\nAXGDMime80zOu0qj3cxTSrwPYY2Gv6tgbZh/ONc+Kk8vFb9+Y+/c5XGcUTtYoQiY\n0yApsQbNXqIN9/FbBlIQy9hordW3rh0YnGHj5TmVLIHpcKtKbFjlxo6aycuREtRp\nBTQq7p0CgYEA3QUMNrKuD1BMvXtpzQt5lGWfyeFaIBryClutrl435iz9BNyMr9Dg\nOHYcyEKwHiw+YLUJYWA60ZWDbfuBW2yKCG5BFpq7/MVFU22v/pQsEoygMzDQZktK\nNDthbChxcPYEceZIU3OckvclznjGN46VxwRH6+t1IDGuI9wRIw/9KWcCgYEA9zDL\nPtpswlzTHlLv1Z0w/VAxhMDO3ePeTeI7R0YOtodouNnOL8KRljrD1ZsbYFJ47ErU\nPpX+OLm69giaOWDFZ4ZMMl0WuSB2EVOnHCQXYS2hnCejCpWQdEJjanXTEbw1XeML\ngXeawuwi74TsKdrbyXy3GAqzxMIafO2MqFl6GPcCgYA79yOiL4ZkJ0A65KIG/McG\nyS+6QUcHkOf8gXU06uE1tR0M1Z3iEcTT7M/QUa+g8BYYfOXHoqkyteML0wH8wQ0O\nToOgU2kPoqI1iXwHkUIH4lmQqfzQ1DqUw0uiYbKtmEIKeRVEdwiTIzUBuOjmp+vh\nLDsrOh30FyaNGicYIT1pnwKBgQDNUAfgosenADaSf0yZXsCsBgm7O/IWtweUJQ4b\newMJdJr0vmPVo4QNBa5XI0evz5CEovp7KVZIg2vYoviGI+ySuidbxZn0FhQ6/AJX\nC1sn6iDLdNilF+ktx16PtGGl329sFgMee9tdf4jc7MjDUvcu+ZmSLIF4MciSbzRf\nOEKDrQKBgBjBrp9Mf67Eh4ztsekhljf4qmmYkMjEAJ1o8DQrMw+AiPGFLeRHTyJo\nM15YcmDg1HDp5YzqnhFERWHoPEEjlrK2b4AMQsHmq0nQoBxCmLhfPFf8hjh7GOnX\nCdVvWz2YvpIs90DMw1jHgJ36qZWrLeQTzlcKNQNCNxmqbwVnTNWp\n-----END RSA PRIVATE KEY-----'
    )]
    for (_id, key) in ls:
        res = sign(_id, key)
        print(res)