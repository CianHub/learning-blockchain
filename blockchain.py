blockchain = []


def get_transaction_value():
    return int(input('Enter a number: '))


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([transaction_amount, last_transaction])


def print_blockchain_blocks():
    for block in blockchain:
        print(block)


transaction_value = get_transaction_value()
add_value(transaction_value)

while True:
    print('Please Choose:')
    print('1: add a new transaction value')
    print('2: Output blockchain blocks')
    user_choice = get_user_choice()

    if user_choice == '1':
        transaction_value = get_transaction_value(),
        add_value(transaction_value, get_last_blockchain_value())

    else:
        print_blockchain_blocks()
