genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
outstanding_transactions = []
owner = 'Cian'
participants = {'Cian'}


def get_transaction_data():
    recipient = input('Enter the recipient: ')
    amount = float(input('Enter the amount of the transaction: '))
    return tuple((recipient, amount))  # Return both as a tuple


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {'sender': sender, 'amount': amount, 'recipient': recipient}
    outstanding_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print(hashed_block)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': outstanding_transactions
    }
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
    return amount_received - amount_sent


def get_amount_sent(participant):
    amount_sent = 0

    # Gets each block in the blockchain, get the transaction property
    # Iterate through the blocks transactions
    # Return a list of values where the provided participant matches the sender property of the transaction
    transactions_where_sender = [
        [transaction['amount'] for transaction in block['transactions']
         if transaction['sender'] == participant]
        for block in blockchain]

    # Iterate through the list and sum the values
    for transaction in transactions_where_sender:
        if len(transaction) > 0:
            amount_sent += transaction[0]

    return amount_sent


def get_amount_received(participant):
    amount_received = 0

    # Gets each block in the blockchain, get the transaction property
    # Iterate through the blocks transactions
    # Return a list of values where the provided participant matches the recipient property of the transaction
    transactions_where_receiver = [
        [transaction['amount'] for transaction in block['transactions']
         if transaction['recipient'] == participant]
        for block in blockchain]

    # Iterate through the list and sum the values
    for transaction in transactions_where_receiver:
        if len(transaction) > 0:
            amount_received += transaction[0]

    return amount_received


def verify_chain():
    # enumerate returns a tuple that contains the value and the index
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        # Compare the previous_hash value of the current block to the hashed previous block
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            # Block is not valid
            return False
    # Block is valid
    return True


waiting_for_input = True

while waiting_for_input:
    print('Please Choose:')
    print('1: Add a new transaction value')
    print('2: Output blockchain blocks')
    print('3: Mine a new block')
    print('4: Output participants')
    print('5: Output your balance')
    print('q: Quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        transaction_data = get_transaction_data()

        recipient, amount = transaction_data  # Pulls out the tuple values
        # Skips optional second argument by using named parameter
        add_transaction(recipient, amount=amount)

    elif user_choice == '2':
        print_blockchain_blocks()

    elif user_choice == '3':
        if mine_block():
            outstanding_transactions = []

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        print(get_balance('Cian'))

    elif user_choice == 'h':
        if len(blockchain):
            blockchain[0] = 2

    elif user_choice == 'q':
        waiting_for_input = False

    else:
        print('Input was invalid, please enter 1 or 2')

    if not verify_chain():
        print('Invalid blockchain')
        waiting_for_input = False
else:
    # While loops can have an else for when the condition isn't true as can for
    print('User has left')

print('Program closing')
