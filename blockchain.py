blockchain = []


def get_user_input():
    return int(input('Enter a number: '))


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([transaction_amount, last_transaction])
    print(blockchain)


add_value(get_user_input())
add_value(last_transaction=get_last_blockchain_value(), transaction_amount=3)
add_value(get_user_input(), [2])
