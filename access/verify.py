from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode, b64decode

def rsa_verify(signature, _id, publicKey):
    sign = b64decode(signature)
    h = SHA.new(_id.encode('utf-8'))
    # keyDER = b64decode(privateKey)
    keyPub = RSA.importKey(publicKey)
    verifier = PKCS1_v1_5.new(keyPub)
    return verifier.verify(h, sign)


if __name__ == '__main__':
    ls = [(
        'D3KeC0bVhgvYnWXeAzXSTF87V0q3/9LRFUr07RzuIMGJ2B36zvYkNkePRSrPZkJ5cFwrUFbgFZBodmN4z3/zA3/YqVxSh7SgZpeGCg7NfSZ5ikU5Q4PosF4rqil7HG7FuIBq6XA6pcPANdD6q+fMfi8hlhwMs/bCPTm7Ax1NDE/n/MHl+7HKX6LfElyRSc8x/q5sVooPfeRfpywV8NlZy/1NqsIywwkeK7H0pw/lYcvr3zGLjcDy4JRASdaD05M1gGPTU7gsZ387mJleJc9AgY4eeBIob/Jm3Cut2azNLU0LVxicJesppG7CpjEzmsA/Z8ZyeBEzYXoCXFn/jS+gCQ==',
        'x',
        '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1Wn/NFUj+K5X+GCzNoqg\nl0K4ZPeSNKaMC7BULn4Mu3p+XawJyL2i/ahjQzauJQiqjju/U0FwteudNcwzuXmo\nh7IXWgdl9QE4iJMsTpOnJvz9IGgW0T2O/PHmhqgDKH/4O/DXIvXW8D/vCOYtNXqy\nuZrYSee5Geo4rwVHpkzijz5H7pGiMYrB8HJzl4046DRBiNDmjZDQSwVsalAGAtzg\nZvNLHqIlybsH4rVKRGzrg3CfnDJiaoqwxaySqij2+5PwmQ/3TlTlLyTiSNRkmA42\nz/slNJheKYUOJhTbIugiYQOweq2lHyiKDq/lDH5gG81A3hUuLSod9tq/VvP2szqa\nYQIDAQAB\n-----END PUBLIC KEY-----'
    )]
    for (sig, _id, key) in ls:
        print(rsa_verify(sig, _id, key))