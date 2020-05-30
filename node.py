from flask import Flask
from flask_cors import CORS

from wallet import Wallet

# Pass Flask the Python file to establish the context in which it runs
app = Flask(__name__)

flask_wallet = Wallet()

# Enable Cross-Origin Resource sharing
CORS(app)


# Registers a new route/endpoint in the Flask App
# Configured to run when a GET req is sent to index
@app.route('/', methods=['GET'])
def get_ui():
    return 'Its working!'


# Will only launch server if node.py is run in its own context
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
