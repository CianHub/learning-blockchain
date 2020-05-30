from flask import Flask, jsonify
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

# Pass Flask the Python file to establish the context in which it runs
app = Flask(__name__)

flask_wallet = Wallet()
blockchain = Blockchain(flask_wallet.public_key)

# Enable Cross-Origin Resource sharing
CORS(app)


# Registers a new route/endpoint in the Flask App
# Configured to run when a GET req is sent to index
@app.route('/', methods=['GET'])
def get_ui():
    return 'Its working!'


@app.route('/chain', methods=['GET'])
def get_blockchain():
    chain = blockchain.chain
    # iterate through blockchain and get a dict for each block
    dict_chain = [block.__dict__.copy() for block in chain]

    # iterate through each block and their transactions and convert each transaction to a dict
    for dict_block in dict_chain:
        dict_block['transactions'] = [transaction.__dict__.copy()
                                      for transaction in dict_block['transactions']]
    return jsonify(dict_chain), 200


    # Will only launch server if node.py is run in its own context
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
