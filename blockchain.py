blockchain = [1]


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount):
    blockchain.append([transaction_amount])
    print(blockchain)


add_value(get_last_blockchain_value())
