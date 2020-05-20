blockchain = []


def get_user_input():
    return int(input('Enter a number: '))


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([transaction_amount, last_transaction])


add_value(get_user_input())

while True:
    add_value(get_user_input(), get_last_blockchain_value())
    for block in blockchain:
        print(block)
