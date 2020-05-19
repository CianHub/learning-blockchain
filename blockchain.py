blockchain = []


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([transaction_amount, last_transaction])
    print(blockchain)


user_amount = int(input('Enter a number: '))
add_value(user_amount)
add_value(last_transaction=get_last_blockchain_value(), transaction_amount=3)
