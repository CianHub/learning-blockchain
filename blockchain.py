blockchain = [1]


def add_value(value):
    blockchain.append([blockchain[-1], value])
    print(blockchain)


add_value(5)
add_value(2)
add_value(4)
