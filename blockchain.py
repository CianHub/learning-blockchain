import functools
import hashlib
from collections import OrderedDict
import json

import hash_util
from block import Block

MINING_REWARD = 10.00
genesis_block = Block(0, '', [], 100, 0)

blockchain = [genesis_block]
outstanding_transactions = []
owner = 'Cian'
participants = {owner}


def get_transaction_data():
    # Return both values  as a tuple
    recipient = input('Enter the recipient: ')
    amount = float(input('Enter the amount of the transaction: '))
    return tuple((recipient, amount))


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    # Creates the transaction dictionary
    # An ordered dict will always have the same order to can be reliably hashed
    # ordered dict consturctor takes a list of tuple key value pairs
    transaction = OrderedDict(
        [('sender', sender), ('amount', amount), ('recipient', recipient)])
    if verify_transaction(transaction):
        outstanding_transactions.append(transaction)
        add_transaction_participants(sender, recipient)
        return True

    return False


def add_transaction_participants(sender, recipient):
    # Adds the sender and recipient to the set of participants
    participants.add(sender)
    participants.add(recipient)


def validate_proof_of_work(transactions, last_hash, proof_number):
    # Create a hash from the outstanding transactions, hash of the block and the proof of work guess number
    # check if the first four digits are 00
    guess = (str(transactions) + str(last_hash) + str(proof_number)).encode()
    guess_hash = hash_util.hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:4] == '0000'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_util.hash_block(last_block)
    proof_number = 0
    while not validate_proof_of_work(outstanding_transactions, last_hash, proof_number):
        proof_number += 1
    return proof_number


def save_blockchain_in_file():
    try:
        with open('blockchain.txt', mode='w') as f:
            hashable_blockchain = [hash_util.create_hashable_block(
                block) for block in blockchain]
            f.write(json.dumps(hashable_blockchain))
            f.write('\n')
            f.write(json.dumps(outstanding_transactions))
    except IOError:
        print('Saving failed')


def load_blockchain_from_file():
    global blockchain
    global outstanding_transactions

    try:
        with open('blockchain.txt', mode='r') as f:
            contents = f.readlines()
            process_loaded_blockchain(json.loads(contents[0][:-1]))
            process_loaded_outstanding_transactions(json.loads(contents[1]))
    except (IOError, IndexError):
        print('File not found, initialising...')
        genesis_block = Block(0, '', [], 100, 0)

        blockchain = [genesis_block]
        outstanding_transactions = []

    finally:
        print('Loading complete')


def process_loaded_blockchain(loaded_blockchain):
    updated_blockchain = []
    # Iterate through the blockchain
    # Iterate through the transactions in each block
    # Return a list of the transactions in block_transactions
    for block in loaded_blockchain:
        block_transactions = [OrderedDict(
            [
                ('sender', transaction['sender']),
                ('amount', transaction['amount']),
                ('recipient', transaction['recipient'])
            ]) for transaction in block['transactions']
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
        global blockchain
        blockchain = updated_blockchain


def process_loaded_outstanding_transactions(loaded_transactions):
    updated_transactions = []
    for transaction in loaded_transactions:
        updated_transaction = OrderedDict(
            [('sender', transaction['sender']), ('amount', transaction['amount']), ('recipient', transaction['recipient'])])
        updated_transactions.append(updated_transaction)
    else:
        global outstanding_transactions
        outstanding_transactions = updated_transactions


def reward_user_for_mining():
    # Adds a new transaction that rewards the user for mining
    # An ordered dict will always have the same order to can be reliably hashed
    # ordered dict consturctor takes a list of tuple key value pairs
    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])

    dup_transactions = outstanding_transactions[:]
    dup_transactions.append(reward_transaction)

    return dup_transactions


def mine_block():
    # Gets the previous block and creates a hash from it
    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)
    proof = proof_of_work()

    # Adds the reward for mining to the outstanding transactions
    dup_transactions = reward_user_for_mining()

    # Creates the new block
    block = Block(len(blockchain), hashed_block, dup_transactions, proof)

    # Adds the new block
    blockchain.append(block)

    return True


def print_blockchain_blocks():
    for block in blockchain:
        print(block)
    else:
        print('-' * 20)


def get_balance(participant):
    amount_sent = get_amount_sent(participant)
    amount_received = get_amount_received(participant)
    outstanding_sent = sum_outstanding_transactions_by_participant_type(
        'sender', participant)
    outstanding_received = sum_outstanding_transactions_by_participant_type(
        'recipient', participant)
    return (outstanding_received + amount_received) - (amount_sent + outstanding_sent)


def get_amount_sent(participant):
    # Gets each block in the blockchain, get the transaction property
    # Iterate through the blocks transactions
    # Return a list of values where the provided participant matches the sender property of the transaction
    transactions_where_sender = [
        [transaction['amount'] for transaction in block.transactions
         if transaction['sender'] == participant]
        for block in blockchain]

    return sum_amounts_list(transactions_where_sender)


def get_amount_received(participant):
    # Gets each block in the blockchain, get the transaction property
    # Iterate through the blocks transactions
    # Return a list of values where the provided participant matches the recipient property of the transaction
    transactions_where_receiver = [
        [transaction['amount'] for transaction in block.transactions
         if transaction['recipient'] == participant]
        for block in blockchain]

    return sum_amounts_list(transactions_where_receiver)


def sum_amounts_list(amount_list):
    # Iterate through the list and sum the values checks if next value is valid before adding
    return functools.reduce(lambda total, next_value: total + sum(next_value)
                            if len(next_value) > 0 else total + 0, amount_list, 0)


def sum_outstanding_transactions_by_participant_type(participant_type, participant):
    return functools.reduce(lambda total, next_value: total +
                            next_value['amount'] if next_value[participant_type] == participant else total + 0, outstanding_transactions, 0)


def verify_chain():
    # enumerate returns a tuple that containing the index and the value
    # Index and block variables are assigned values from enumarate
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        # Compare the previous_hash value of the current block to the hashed previous block
        if block.previous_hash != hash_util.hash_block(blockchain[index - 1]):
            # Block is not valid
            return False
        if not validate_proof_of_work(block.transactions[:-1], block.previous_hash, block.proof):
            # Block is not valid
            return False

    # Block is valid
    return True


def verify_transactions_validity():
    return all([verify_transaction(transaction) for transaction in outstanding_transactions])


def verify_transaction(transaction):
    # Get the senders balance and return if they have enough to make a transaction
    return get_balance(transaction['sender']) >= transaction['amount']


waiting_for_input = True

while waiting_for_input:
    load_blockchain_from_file()
    print('Please Choose:')
    print('1: Add a new transaction value')
    print('2: Output blockchain blocks')
    print('3: Mine a new block')
    print('4: Output participants')
    print('5: Output your balance')
    print('6: Check outstanding transaction validity')
    print('q: Quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        transaction_data = get_transaction_data()

        # Pulls out the tuple values
        recipient, amount = transaction_data

        # Skips optional second argument by naming parameter
        if add_transaction(recipient, amount=amount):
            save_blockchain_in_file()
            print('Transaction Successful')
        else:
            print('Insufficient Balance To Make Transaction')

    elif user_choice == '2':
        print_blockchain_blocks()

    elif user_choice == '3':
        # Resets outstanding transactions on successful mining
        if mine_block():
            outstanding_transactions = []
            save_blockchain_in_file()

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        if get_balance(owner):
            print(f'{owner}\'s balance is: {get_balance(owner):6.2f}')

    elif user_choice == '6':
        if verify_transactions_validity():
            print('All transactions valid')
        else:
            print('Invalid transactions present')

    elif user_choice == 'q':
        waiting_for_input = False

    else:
        print('Input was invalid, please enter a valid option')

    if not verify_chain():
        print('Invalid blockchain')
        waiting_for_input = False
else:
    # While loops can have an else for when the condition isn't true as can for
    print('User has left')

print('Program closing')
