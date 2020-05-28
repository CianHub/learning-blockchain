from utility import hash_util, verification
from utility.verification import Verification

from blockchain import Blockchain
from wallet import Wallet

from uuid import uuid4


class Node:

    def __init__(self):
        self.wallet = Wallet()
        self.waiting_for_input = True
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
        self.verifier = Verification()

    def listen_for_input(self):
        while self.waiting_for_input:
            self.blockchain.load_blockchain_from_file()
            print('Please Choose:')
            print('1: Add a new transaction value')
            print('2: Output blockchain blocks')
            print('3: Mine a new block')
            print('4: Output your balance')
            print('5: Check outstanding transaction validity')
            print('6: Create wallet')
            print('7: Load wallet')
            print('8: Save wallet keys')
            print('q: Quit')
            user_choice = self.get_user_choice()

            if user_choice == '1':
                transaction_data = self.get_transaction_data()

                # Pulls out the tuple values
                recipient, amount = transaction_data

                # Skips optional second argument by naming parameter
                if self.blockchain.add_transaction(recipient, self.wallet.public_key,  amount=amount):
                    self.blockchain.save_blockchain_in_file()
                    print('Transaction Successful')
                else:
                    print('Insufficient Balance To Make Transaction')

            elif user_choice == '2':
                self.blockchain.print_blockchain_blocks()

            elif user_choice == '3':
                # Resets outstanding transactions on successful mining
                if self.blockchain.mine_block(self.wallet.public_key):
                    self.blockchain.save_blockchain_in_file()
                else:
                    print('Mining failed. Please check you have a wallet.')

            elif user_choice == '4':
                if self.verifier.get_balance(self.wallet.public_key, self.blockchain.outstanding_transactions, self.blockchain.chain):
                    print(
                        f'{self.wallet.public_key}\'s balance is: {self.verifier.get_balance(self.wallet.public_key, self.blockchain.outstanding_transactions, self.blockchain.chain):6.2f}')

            elif user_choice == '5':
                if self.verifier.verify_transactions_validity(self.blockchain.outstanding_transactions, self.blockchain.chain):
                    print('All transactions valid')
                else:
                    print('Invalid transactions present')

            elif user_choice == '6':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
                print('CREATING KEYS...')

            elif user_choice == '7':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
                print('LOADING KEYS...')

            elif user_choice == '8':
                self.wallet.save_keys()
                print('SAVING KEYS...')

            elif user_choice == 'q':
                self.waiting_for_input = False

            else:
                print('Input was invalid, please enter a valid option')

            if not self.verifier.verify_chain(self.blockchain.chain):
                print('Invalid blockchain')
                self.waiting_for_input = False

        else:
            # While loops can have an else for when the condition isn't true as can for
            print('User has left')

        print('Program closing')

    def get_transaction_data(self):
        # Return both values  as a tuple
        recipient = input('Enter the recipient: ')
        amount = float(input('Enter the amount of the transaction: '))
        return tuple((recipient, amount))

    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input

    def get_last_blockchain_value(self, blockchain):
        if len(blockchain) < 1:
            return None

        return blockchain[-1]


node1 = Node()
node1.listen_for_input()
