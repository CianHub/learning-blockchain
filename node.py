from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain
from utility.verification import Verification

# Pass Flask the Python file to establish the context in which it runs
app = Flask(__name__)

flask_wallet = Wallet()
blockchain = Blockchain(flask_wallet.public_key)
verification = Verification()

# Enable Cross-Origin Resource sharing
CORS(app)


# Registers a new route/endpoint in the Flask App
# Configured to run when a GET req is sent to index
@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Block added successfully.',
            'block': dict_block,
            'funds': verification.get_balance(flask_wallet.public_key, blockchain.outstanding_transactions, blockchain.chain)

        }

        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed.',
            'wallet_set_up': flask_wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/transactions', methods=['GET'])
def get_outstanding_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [transaction.__dict__ for transaction in transactions]

    return jsonify(dict_transactions), 200


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if flask_wallet.public_key == None:
        response = {
            'message': 'No wallet found'
        }
        return jsonify(response), 400

    values = request.get_json()

    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400

    required_fields = ['recipient', 'amount']

    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing'
        }
        return jsonify(response), 400

    recipient = values['recipient']
    amount = values['amount']
    signature = flask_wallet.sign_transaction(
        flask_wallet.public_key, recipient, amount)

    success = blockchain.add_transaction(
        signature, recipient, flask_wallet.public_key, amount)

    if success:
        response = {
            'message': 'Add transaction succeeded',
            'transaction': {
                'sender': flask_wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': verification.get_balance(flask_wallet.public_key, blockchain.outstanding_transactions, blockchain.chain)
        }
        return jsonify(response), 201

    else:
        response = {
            'message': 'Add transaction failed'
        }
        return jsonify(response), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = verification.get_balance(
        flask_wallet.public_key, blockchain.outstanding_transactions, blockchain.chain)

    if balance != None:
        response = {
            'response': 'fetched balance',
            'balance': balance
        }
        return jsonify(response), 201

    else:
        response = {
            'response': 'Loading balance failed',
            'wallet_set_up': flask_wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_blockchain():
    chain = blockchain.convert_blockchain_to_json()
    return jsonify(chain), 200


@app.route('/wallet', methods=['POST'])
def create_keys():
    flask_wallet.create_keys()

    if flask_wallet.save_keys():
        global blockchain
        blockchain = Blockchain(flask_wallet.public_key)
        response = {
            'public_key': flask_wallet.public_key,
            'private_key': flask_wallet.private_key,
            'funds': verification.get_balance(flask_wallet.public_key, blockchain.outstanding_transactions, blockchain.chain)
        }

        return jsonify(response), 201

    else:
        response = {
            'message': 'Saving the keys failed.'
        }
        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if flask_wallet.load_keys():
        global blockchain
        blockchain = Blockchain(flask_wallet.public_key)
        response = {
            'public_key': flask_wallet.public_key,
            'private_key': flask_wallet.private_key,
            'funds': verification.get_balance(flask_wallet.public_key, blockchain.outstanding_transactions, blockchain.chain)
        }

        return jsonify(response), 201
    else:
        response = {
            'message': 'Loading the keys failed.'
        }
        return jsonify(response), 500


# Will only launch server if node.py is run in its own context
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
