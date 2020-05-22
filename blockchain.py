MINING_REWARD = 10.00
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
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
    transaction = {'sender': sender, 'amount': amount, 'recipient': recipient}

    if verify_transaction(transaction):
        outstanding_transactions.append(transaction)
        add_transaction_participants(sender, recipient)
        return True

    return False


def add_transaction_participants(sender, recipient):
    # Adds the sender and recipient to the set of participants
    participants.add(sender)
    participants.add(recipient)


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def reward_user_for_mining():
    # Adds a new transaction that rewards the user for mining
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }

    dup_transactions = outstanding_transactions[:]
    dup_transactions.append(reward_transaction)

    return dup_transactions


def mine_block():
    # Gets the previous block and creates a hash from it
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    # Adds the reward for mining to the outstanding transactions
    dup_transactions = reward_user_for_mining()

    # Creates the new block
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': dup_transactions
    }

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
    outstanding_sent = get_outstanding_transaction_amount_sent_for_user(
        participant)
    outstanding_received = get_outstanding_transaction_amount_received_for_user(
        participant)
    return (outstanding_received + amount_received) - (amount_sent + outstanding_sent)


def get_outstanding_transaction_amount_sent_for_user(participant):
    outstanding_transactions_where_sender_amount = 0

    for transaction in outstanding_transactions:
        if transaction['sender'] == participant:
            outstanding_transactions_where_sender_amount += transaction['amount']

    return outstanding_transactions_where_sender_amount


def get_outstanding_transaction_amount_received_for_user(participant):
    outstanding_transactions_where_recipient_amount = 0

    for transaction in outstanding_transactions:
        if transaction['recipient'] == participant:
            outstanding_transactions_where_sender_amount += transaction['amount']

    return outstanding_transactions_where_recipient_amount


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
    # enumerate returns a tuple that containing the index and the value
    # Index and block variables are assigned values from enumarate
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        # Compare the previous_hash value of the current block to the hashed previous block
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
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
            print('Transaction Successful')
        else:
            print('Insufficient Balance To Make Transaction')

    elif user_choice == '2':
        print_blockchain_blocks()

    elif user_choice == '3':
        # Resets outstanding transactions on successful mining
        if mine_block():
            outstanding_transactions = []

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        if get_balance(owner):
            print(get_balance(owner))

    elif user_choice == '6':
        if verify_transactions_validity():
            print('All transactions valid')
        else:
            print('Invalid transactions present')

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
