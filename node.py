from verification import Verification
from blockchain import Blockchain

from uuid import uuid4


class Node:

    def __init__(self):
        self.id = str(uuid4())
        self.waiting_for_input = True
        self.blockchain = Blockchain(self.id)
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
            print('q: Quit')
            user_choice = self.get_user_choice()

            if user_choice == '1':
                transaction_data = self.get_transaction_data()

                # Pulls out the tuple values
                recipient, amount = transaction_data

                # Skips optional second argument by naming parameter
                if self.blockchain.add_transaction(recipient, self.id,  amount=amount):
                    self.blockchain.save_blockchain_in_file()
                    print('Transaction Successful')
                else:
                    print('Insufficient Balance To Make Transaction')

            elif user_choice == '2':
                self.blockchain.print_blockchain_blocks()

            elif user_choice == '3':
                # Resets outstanding transactions on successful mining
                if self.blockchain.mine_block(self.id):
                    self.blockchain.outstanding_transactions = []
                    self.blockchain.save_blockchain_in_file()

            elif user_choice == '4':
                if self.verifier.get_balance(self.id, self.blockchain.outstanding_transactions, self.blockchain.chain):
                    print(
                        f'{self.id}\'s balance is: {self.verifier.get_balance(self.id, self.blockchain.outstanding_transactions, self.blockchain.chain):6.2f}')

            elif user_choice == '5':
                if self.verifier.verify_transactions_validity(self.blockchain.outstanding_transactions, self.blockchain.chain):
                    print('All transactions valid')
                else:
                    print('Invalid transactions present')

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
