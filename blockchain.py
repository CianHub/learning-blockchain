blockchain = []
outstanding_transactions = []
owner = 'Cian'


def get_transaction_data():
    recipient = input('Enter the recipient: ')
    amount = float(input('Enter the amount of the transaction: '))
    return (recipient, amount)  # Return both as a tuple


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    if last_transaction == None:
        last_transaction = [1]

    transaction = {'sender': sender, 'amount': amount, 'recipient': recipient}
    outstanding_transactions.append(transaction)


def mine_block():
    pass


def print_blockchain_blocks():
    for block in blockchain:
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        # Checks if the first element of a block is equal to the entire previous block
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break

    return is_valid


waiting_for_input = True

while waiting_for_input:
    print('Please Choose:')
    print('1: add a new transaction value')
    print('2: Output blockchain blocks')
    print('q: quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        transaction_data = get_transaction_data(),
        recipient, amount = transaction_data  # Pulls out the tuple values
        # Skips optional second argument by using named parameter
        add_transaction(recipient, amount=amount)

    elif user_choice == '2':
        print_blockchain_blocks()

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
