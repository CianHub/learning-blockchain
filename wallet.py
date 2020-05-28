from Crypto.PublicKey import RSA
import Crypto.Random
import binascii


class Wallet:
    def __init__(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def generate_keys(self):
        # Generate a private key with the RSA algorithim to be 1024 bits
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        # keys are in binary so need to convert them
        return (binascii.hexlify(private_key.export_key(format='DER')).decode('ascii'), binascii.hexlify(public_key.export_key(format='DER')).decode('ascii'))
