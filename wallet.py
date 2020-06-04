from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    def __init__(self, node_id):
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    def generate_keys(self):
        # Generate a private key with the RSA algorithim to be 1024 bits
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        # keys are in binary so need to convert them
        return (binascii.hexlify(private_key.export_key(format='DER')).decode('ascii'), binascii.hexlify(public_key.export_key(format='DER')).decode('ascii'))

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet-{}.txt'.format(self.node_id), mode='w')as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                return True
            except (IOError, IndexError):
                print('Saving wallet failed')
                return False

    def load_keys(self):
        try:
            with open('wallet-{}.txt'.format(self.node_id), mode='r')as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
            return True
        except (IOError, IndexError):
            print('Loading wallet failed')
            return False

    def sign_transaction(self, sender, recipient, amount):
        signer_id = pkcs1_15.new(RSA.import_key(
            binascii.unhexlify(self.private_key)))
        hashed_transaction = SHA256.new((
            str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer_id.sign(hashed_transaction)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        if transaction.sender == 'MINING':
            return True

        public_key = RSA.import_key(binascii.unhexlify(transaction.sender))
        verification_checker = pkcs1_15.new(public_key)
        hashed_transaction = SHA256.new((
            str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verification_checker.verify(hashed_transaction, binascii.unhexlify(transaction.signature))
