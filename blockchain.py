import functools
import hashlib
from collections import OrderedDict
import json

import hash_util
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10.00
genesis_block = Block(0, '', [], 100, 0)

blockchain = [genesis_block]
outstanding_transactions = []
owner = 'Cian'
participants = {owner}

verify = Verification()


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
    transaction = Transaction(sender, recipient, amount)
    if verify.verify_transaction(transaction, outstanding_transactions, blockchain):
        outstanding_transactions.append(transaction)
        add_transaction_participants(sender, recipient)
        return True

    return False


def add_transaction_participants(sender, recipient):
    # Adds the sender and recipient to the set of participants
    participants.add(sender)
    participants.add(recipient)


def save_blockchain_in_file():
    try:
        with open('blockchain.txt', mode='w') as f:
            hashable_blockchain = hash_util.create_hashable_blockchain(
                blockchain)
            hashable_transactions = hash_util.create_hashable_obj_list(
                outstanding_transactions)

            f.write(json.dumps(hashable_blockchain))
            f.write('\n')
            f.write(json.dumps(hashable_transactions))
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
        global blockchain
        blockchain = updated_blockchain


def process_loaded_outstanding_transactions(loaded_transactions):
    updated_transactions = []
    for transaction in loaded_transactions:
        updated_transaction = Transaction(
            transaction['sender'], transaction['recipient'], transaction['amount'])
        updated_transactions.append(updated_transaction)
    else:
        global outstanding_transactions
        outstanding_transactions = updated_transactions


def reward_user_for_mining():
    # Adds a new transaction that rewards the user for mining
    # An ordered dict will always have the same order to can be reliably hashed
    # ordered dict consturctor takes a list of tuple key value pairs
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    dup_transactions = outstanding_transactions[:]
    dup_transactions.append(reward_transaction)

    return dup_transactions


def mine_block():
    # Gets the previous block and creates a hash from it
    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)
    proof = verify.proof_of_work(blockchain, outstanding_transactions)

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
        if verify.get_balance(owner, outstanding_transactions, blockchain):
            print(
                f'{owner}\'s balance is: {verify.get_balance(owner, outstanding_transactions,blockchain):6.2f}')

    elif user_choice == '6':
        if verify.verify_transactions_validity(outstanding_transactions, blockchain):
            print('All transactions valid')
        else:
            print('Invalid transactions present')

    elif user_choice == 'q':
        waiting_for_input = False

    else:
        print('Input was invalid, please enter a valid option')

    if not verify.verify_chain(blockchain):
        print('Invalid blockchain')
        waiting_for_input = False
else:
    # While loops can have an else for when the condition isn't true as can for
    print('User has left')

print('Program closing')
