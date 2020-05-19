blockchain = []


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([transaction_amount, last_transaction])
    print(blockchain)


add_value(1)
add_value(3, get_last_blockchain_value())
