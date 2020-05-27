import functools
import hashlib
from collections import OrderedDict
import json

import hash_util
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10.00


class Blockchain:

    def __init__(self, host_node_id):
        self.genesis_block = Block(0, '', [], 100, 0)
        self.chain = [self.genesis_block]
        self.outstanding_transactions = []
        self.verification = Verification()
        self.hostNode = host_node_id

    def add_transaction(self, recipient, sender, amount=1.0):
        # Creates the transaction dictionary
        # An ordered dict will always have the same order to can be reliably hashed
        # ordered dict consturctor takes a list of tuple key value pairs
        transaction = Transaction(sender, recipient, amount)
        if self.verification.verify_transaction(transaction, self.outstanding_transactions, self.chain):
            self.outstanding_transactions.append(transaction)
            return True

        return False

    def save_blockchain_in_file(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                hashable_blockchain = hash_util.create_hashable_blockchain(
                    self.chain)
                hashable_transactions = hash_util.create_hashable_obj_list(
                    self.outstanding_transactions)

                f.write(json.dumps(hashable_blockchain))
                f.write('\n')
                f.write(json.dumps(hashable_transactions))
        except IOError:
            print('Saving failed')

    def load_blockchain_from_file(self):

        try:
            with open('blockchain.txt', mode='r') as f:
                contents = f.readlines()
                self.process_loaded_blockchain(json.loads(contents[0][:-1]))
                self.process_loaded_outstanding_transactions(
                    json.loads(contents[1]))
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
                transaction['sender'], transaction['recipient'], transaction['amount'])
            updated_transactions.append(updated_transaction)
        else:
            self.outstanding_transactions = updated_transactions

    def reward_user_for_mining(self):
        # Adds a new transaction that rewards the user for mining
        # An ordered dict will always have the same order to can be reliably hashed
        # ordered dict consturctor takes a list of tuple key value pairs
        reward_transaction = Transaction(
            'MINING', self.hostNode, MINING_REWARD)
        dup_transactions = self.outstanding_transactions[:]
        dup_transactions.append(reward_transaction)

        return dup_transactions

    def mine_block(self, sender):
        # Gets the previous block and creates a hash from it
        last_block = self.chain[-1]
        hashed_block = hash_util.hash_block(last_block)
        proof = self.verification.proof_of_work(
            self.chain, self.outstanding_transactions)

        # Adds the reward for mining to the outstanding transactions
        dup_transactions = self.reward_user_for_mining()

        # Creates the new block
        block = Block(len(self.chain), hashed_block, dup_transactions, proof)

        # Adds the new block
        self.chain.append(block)

        return True

    def print_blockchain_blocks(self):
        for block in self.chain:
            print(block)
        else:
            print('-' * 20)
