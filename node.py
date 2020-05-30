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


@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.mine_block()
    if block != None:
        response = {
            'message': 'Block added successfully',
            'block': blockchain.convert_block_transactions_to_json(block)
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed.',
            'wallet_set_up': flask_wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_blockchain():
    chain = blockchain.convert_blockchain_to_json()

    return jsonify(chain), 200


    # Will only launch server if node.py is run in its own context
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
