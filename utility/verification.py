""" Provides helper methods for verification """

from utility import hash_util
from wallet import Wallet

import functools


class Verification:

    @staticmethod
    def validate_proof_of_work(transactions, last_hash, proof_number):
        # Create a hash from the outstanding transactions, hash of the block and the proof of work guess number
        # check if the first four digits are 00
        guess = (str([transaction.to_ordered_dict() for transaction in transactions]
                     ) + str(last_hash) + str(proof_number)).encode()
        guess_hash = hash_util.hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:4] == '0000'

    @classmethod
    def proof_of_work(cls, blockchain, outstanding_transactions):
        last_block = blockchain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof_number = 0
        while not cls.validate_proof_of_work(outstanding_transactions, last_hash, proof_number):
            proof_number += 1
        return proof_number

    @classmethod
    def verify_transactions_validity(cls, outstanding_transactions, blockchain):
        return all([cls.verify_transaction(transaction, outstanding_transactions, blockchain, False) for transaction in outstanding_transactions])

    @classmethod
    def verify_transaction(cls, transaction, outstanding_transactions, blockchain, check_funds=True):
        if check_funds:
            # Get the senders balance and return if they have enough to make a transaction
            return cls.get_balance(transaction.sender, outstanding_transactions, blockchain) >= transaction.amount
        return Wallet.verify_transaction(transaction)

    @classmethod
    def get_balance(cls, participant, outstanding_transactions, blockchain, sender=None):

        if sender == None:
            if blockchain.public_key == None:
                return None
            participant = blockchain.public_key
        else:
            participant == sender

        if participant == None:
            return None
        else:
            amount_sent = cls.get_amount_sent(participant, blockchain)
            amount_received = cls.get_amount_received(participant, blockchain)
            outstanding_sent = cls.sum_outstanding_transactions_by_sender(
                participant, outstanding_transactions)
            outstanding_received = cls.sum_outstanding_transactions_by_recipient(
                participant, outstanding_transactions)
            return (outstanding_received + amount_received) - (amount_sent + outstanding_sent)

    @classmethod
    def get_amount_sent(cls, participant, blockchain):
        # Gets each block in the blockchain, get the transaction property
        # Iterate through the blocks transactions
        # Return a list of values where the provided participant matches the sender property of the transaction
        transactions_where_sender = [
            [transaction.amount for transaction in block.transactions
             if transaction.sender == participant]
            for block in blockchain]

        return cls.sum_amounts_list(transactions_where_sender)

    @classmethod
    def get_amount_received(cls, participant, blockchain):
        # Gets each block in the blockchain, get the transaction property
        # Iterate through the blocks transactions
        # Return a list of values where the provided participant matches the recipient property of the transaction
        transactions_where_receiver = [
            [transaction.amount for transaction in block.transactions
             if transaction.recipient == participant]
            for block in blockchain]

        return cls.sum_amounts_list(transactions_where_receiver)

    @staticmethod
    def sum_amounts_list(amount_list):
        # Iterate through the list and sum the values checks if next value is valid before adding
        return functools.reduce(lambda total, next_value: total + sum(next_value)
                                if len(next_value) > 0 else total + 0, amount_list, 0)

    @staticmethod
    def sum_outstanding_transactions_by_sender(participant, outstanding_transactions):
        return functools.reduce(lambda total, next_value: total +
                                next_value.amount if next_value.sender == participant else total + 0, outstanding_transactions, 0)

    @staticmethod
    def sum_outstanding_transactions_by_recipient(participant, outstanding_transactions):
        return functools.reduce(lambda total, next_value: total +
                                next_value.amount if next_value.recipient == participant else total + 0, outstanding_transactions, 0)

    @classmethod
    def verify_chain(cls, blockchain):
        # enumerate returns a tuple that containing the index and the value
        # Index and block variables are assigned values from enumarate
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            # Compare the previous_hash value of the current block to the hashed previous block
            if block.previous_hash != hash_util.hash_block(blockchain[index - 1]):
                # Block is not valid
                return False
            if not cls.validate_proof_of_work(block.transactions[:-1], block.previous_hash, block.proof):
                # Block is not valid
                return False

        # Block is valid
        return True
