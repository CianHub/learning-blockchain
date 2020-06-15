import functools
import hashlib
from collections import OrderedDict
import json
import requests

from utility import hash_util, verification
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

MINING_REWARD = 10.00


class Blockchain:

    def __init__(self, node_id, host_node_public_key):
        self.genesis_block = Block(0, '', [], 100, 0)
        self.chain = [self.genesis_block]
        self.outstanding_transactions = []
        self.verification = Verification()
        self.host_node_public_key = host_node_public_key
        self.node_id = node_id
        self.__peer_nodes = set()
        self.load_blockchain_from_file()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    @property
    def outstanding_transactions(self):
        return self.__outstanding_transactions[:]

    @outstanding_transactions.setter
    def outstanding_transactions(self, val):
        self.__outstanding_transactions = val

    def add_transaction(self, signature, recipient, sender, amount=1.0, is_receiving=False):
        if self.host_node_public_key == None:
            return False

        print(self.host_node_public_key)
        # Creates the transaction dictionary
        # An ordered dict will always have the same order to can be reliably hashed
        # ordered dict consturctor takes a list of tuple key value pairs
        transaction = Transaction(sender, recipient, amount, signature)

        if self.verification.verify_transaction(transaction, self.__outstanding_transactions, self.__chain):
            self.__outstanding_transactions.append(transaction)
            self.save_blockchain_in_file()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    response = requests.post(url, json={
                        "sender": sender, "recipient": recipient, "amount": amount, "signature": signature})
                    try:
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def save_blockchain_in_file(self):
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f:
                hashable_blockchain = hash_util.create_hashable_blockchain(
                    self.__chain)
                hashable_transactions = hash_util.create_hashable_obj_list(
                    self.__outstanding_transactions)

                f.write(json.dumps(hashable_blockchain))
                f.write('\n')
                f.write(json.dumps(hashable_transactions))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))

        except IOError:
            print('Saving failed')

    def load_blockchain_from_file(self):

        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f:
                contents = f.readlines()
                self.process_loaded_blockchain(json.loads(contents[0][:-1]))
                self.process_loaded_outstanding_transactions(
                    json.loads(contents[1][:-1]))
                self.process_loaded_peer_nodes(json.loads(contents[2]))
        except (IOError, IndexError):
            print('File not found, initialising...')

        finally:
            print('Loading complete')

    def process_loaded_blockchain(self, loaded_blockchain):
        updated_blockchain = []
        # Iterate through the blockchain
        # Iterate through the transactions in each block
        # Return a list of the transactions in block_transactions
        for block in loaded_blockchain:
            block_transactions = [Transaction(
                transaction['sender'],
                transaction['recipient'],
                transaction['amount'],
                transaction['signature']
            ) for transaction in block['transactions']
            ]

            # Create a new Block instance from the loaded data
            updated_block = Block(
                block['index'],
                block['previous_hash'],
                block_transactions,
                block['proof'],
                block['timestamp'])

            updated_blockchain.append(updated_block)
        else:
            self.chain = updated_blockchain

    def process_loaded_outstanding_transactions(self, loaded_transactions):
        updated_transactions = []
        for transaction in loaded_transactions:
            updated_transaction = Transaction(
                transaction['sender'], transaction['recipient'], transaction['amount'], transaction['signature'])
            updated_transactions.append(updated_transaction)
        else:
            self.outstanding_transactions = updated_transactions

    def process_loaded_peer_nodes(self, loaded_peer_nodes):
        self.__peer_nodes = set(loaded_peer_nodes)

    def reward_user_for_mining(self):
        # Adds a new transaction that rewards the user for mining
        # An ordered dict will always have the same order to can be reliably hashed
        # ordered dict consturctor takes a list of tuple key value pairs
        reward_transaction = Transaction(
            'MINING', self.host_node_public_key, MINING_REWARD, '')
        dup_transactions = self.__outstanding_transactions[:]
        dup_transactions.append(reward_transaction)

        return dup_transactions

    def mine_block(self):
        if self.host_node_public_key != None:

            for transaction in self.__chain[-1].transactions[:]:
                # Check transaction signatures are valid
                if not Wallet.verify_transaction(transaction):
                    return None

            # Gets the previous block and creates a hash from it
            last_block = self.__chain[-1]
            hashed_block = hash_util.hash_block(last_block)
            proof = self.verification.proof_of_work(
                self.__chain, self.__outstanding_transactions)

            # Adds the reward for mining to the outstanding transactions
            dup_transactions = self.reward_user_for_mining()

            # Creates the new block
            block = Block(len(self.__chain), hashed_block,
                          dup_transactions, proof)

            # Adds the new block
            self.__chain.append(block)

            self.outstanding_transactions = []

            return block

    def print_blockchain_blocks(self):
        for block in self.__chain:
            print(block)
        else:
            print('-' * 20)

    def convert_blockchain_to_json(self):
        # iterate through blockchain and get a dict for each block
        dict_chain = [block.__dict__.copy() for block in self.chain]

        # iterate through each block and their transactions and convert each transaction to a dict
        for dict_block in dict_chain:
            dict_block = self.convert_block_transactions_to_json(dict_block)

        return dict_chain

    def convert_block_transactions_to_json(self, block):
        block['transactions'] = [
            transaction.__dict__.copy() for transaction in block['transactions']]

        return block

    def add_peer_node(self, node):
        # adds a new node to the peer_node set
        # Takes in node IP
        self.__peer_nodes.add(node)
        self.save_blockchain_in_file()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_blockchain_in_file()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)
