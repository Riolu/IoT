import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
from base64 import b64encode, b64decode


def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    random_generator = Random.new().read
    new_key = RSA.generate(bits, random_generator)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    return str(private_key), str(public_key)


def main():
    for _ in range(10):
        private_key, public_key = generate_RSA()
        print(b64decode(private_key))
        print(b64decode(public_key))
        print('-' * 20)


if __name__ == '__main__':
    main()
