blockchain = []


def get_transaction_value():
    return int(input('Enter a number: '))


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction):
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([transaction_amount, last_transaction])


def print_blockchain_blocks():
    for block in blockchain:
        print(block)


while True:
    print('Please Choose:')
    print('1: add a new transaction value')
    print('2: Output blockchain blocks')
    print('q: quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        transaction_value = get_transaction_value(),
        add_transaction(transaction_value, get_last_blockchain_value())

    elif user_choice == '2':
        print_blockchain_blocks()

    elif user_choice == 'q':
        break

    else:
        print('Input was invalid, please enter 1 or 2')

    print('Choice registered')


print('Program closing')
