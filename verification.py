import hash_util
import functools


class Verification:

    def validate_proof_of_work(self, transactions, last_hash, proof_number):
        # Create a hash from the outstanding transactions, hash of the block and the proof of work guess number
        # check if the first four digits are 00
        guess = (str([transaction.to_ordered_dict() for transaction in transactions]
                     ) + str(last_hash) + str(proof_number)).encode()
        guess_hash = hash_util.hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:4] == '0000'

    def proof_of_work(self, blockchain, outstanding_transactions):
        last_block = blockchain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof_number = 0
        while not self.validate_proof_of_work(outstanding_transactions, last_hash, proof_number):
            proof_number += 1
        return proof_number

    def verify_transactions_validity(self, outstanding_transactions, blockchain):
        return all([self.verify_transaction(transaction, outstanding_transactions, blockchain) for transaction in outstanding_transactions])

    def verify_transaction(self, transaction, outstanding_transactions, blockchain):
        # Get the senders balance and return if they have enough to make a transaction
        return self.get_balance(transaction.sender, outstanding_transactions, blockchain) >= transaction.amount

    def get_balance(self, participant, outstanding_transactions, blockchain):
        amount_sent = self.get_amount_sent(participant, blockchain)
        amount_received = self.get_amount_received(participant, blockchain)
        outstanding_sent = self.sum_outstanding_transactions_by_sender(
            participant, outstanding_transactions)
        outstanding_received = self.sum_outstanding_transactions_by_recipient(
            participant, outstanding_transactions)
        return (outstanding_received + amount_received) - (amount_sent + outstanding_sent)

    def get_amount_sent(self, participant, blockchain):
        # Gets each block in the blockchain, get the transaction property
        # Iterate through the blocks transactions
        # Return a list of values where the provided participant matches the sender property of the transaction
        transactions_where_sender = [
            [transaction.amount for transaction in block.transactions
             if transaction.sender == participant]
            for block in blockchain]

        return self.sum_amounts_list(transactions_where_sender)

    def get_amount_received(self, participant, blockchain):
        # Gets each block in the blockchain, get the transaction property
        # Iterate through the blocks transactions
        # Return a list of values where the provided participant matches the recipient property of the transaction
        transactions_where_receiver = [
            [transaction.amount for transaction in block.transactions
             if transaction.recipient == participant]
            for block in blockchain]

        return self.sum_amounts_list(transactions_where_receiver)

    def sum_amounts_list(self, amount_list):
        # Iterate through the list and sum the values checks if next value is valid before adding
        return functools.reduce(lambda total, next_value: total + sum(next_value)
                                if len(next_value) > 0 else total + 0, amount_list, 0)

    def sum_outstanding_transactions_by_sender(self, participant, outstanding_transactions):
        return functools.reduce(lambda total, next_value: total +
                                next_value.amount if next_value.sender == participant else total + 0, outstanding_transactions, 0)

    def sum_outstanding_transactions_by_recipient(self, participant, outstanding_transactions):
        return functools.reduce(lambda total, next_value: total +
                                next_value.amount if next_value.recipient == participant else total + 0, outstanding_transactions, 0)

    def verify_chain(self, blockchain):
        # enumerate returns a tuple that containing the index and the value
        # Index and block variables are assigned values from enumarate
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            # Compare the previous_hash value of the current block to the hashed previous block
            if block.previous_hash != hash_util.hash_block(blockchain[index - 1]):
                # Block is not valid
                return False
            if not self.validate_proof_of_work(block.transactions[:-1], block.previous_hash, block.proof):
                # Block is not valid
                return False

        # Block is valid
        return True
