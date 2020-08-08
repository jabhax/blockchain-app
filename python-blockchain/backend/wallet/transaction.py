import time
import uuid

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT


class Transaction:
    '''
        Document of an exchange in currency from a sender to one or more
        recipients.
    '''

    def __init__(self, sender_wallet=None, recipient=None,
                amount=None, id=None, output=None, input=None):
        '''
            A transaction consists of an input and output field.

            id:     Transaction ID represented as the first 8 characters
                    generated by the uuid4 python module.
            Input:  The input contains metadata, including the address, public
                    key, and the balance amount of the sender. The input also
                    includes a signature that's generated by the sender, using
                    the transaction output as the underlying data.
            Output: The output contains a series of entries where recipient
                    addresses will receive certain amounts as a result of the
                    transaction. The transaction can have any number of
                    recipients. At least one of the recipients is the sender
                    address itself, because this details how much currency the
                    sender should have after the transaction is completed.
        '''
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(sender_wallet, recipient, amount)
        self.input = input or self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, recipient, amount):
        '''
            Structure the output data for the transaction.

            Params:
                sender_wallet - (Wallet): a Block's Wallet.
                recipient - (String): a representation of the recipient as a
                                      String.
                amount - (int): the amount of the transaction.
        '''
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds recipient balance')
        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = (sender_wallet.balance - amount)
        return output

    def create_input(self, sender_wallet, output):
        '''
            Structure the input data for the transaction.
            Sign the transaction and include the sender's public key and address.

            Params:
                sender_wallet - (Wallet): a Block's Wallet.
                output - (json): contains key-value pairs of
                                (recipient, amount), (address, updated-balance)
        '''
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    def update(self, sender_wallet, recipient, amount):
        '''
            Update the Transaction with an existing or new recipient.
        '''
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds the amount provided by sender '
                            'block wallet.')
        # Check if the recipient is in the Block's Transaction output.
        # If it is then we simply update the recipient's transaction amount,
        if recipient in self.output:
            self.output[recipient] += amount
        else:
        # Else it is a new recipient and the amount will be their set amount.
            self.output[recipient] = amount
        # Update the sender block's address with the change-in-transaction
        # amount.
        self.output[sender_wallet.address] -= amount
        # Re-sign the transaction by creating new, signed, and valid input.
        self.input = self.create_input(sender_wallet, self.output)

    def to_json(self):
        ''' Serialize a Transaction object into json '''
        return self.__dict__

    @staticmethod
    def from_json(trans_json):
        '''
        De-serialize a transaction's json representation back into Transaction Instance
        '''
        return Transaction(**trans_json)

    @staticmethod
    def is_valid(transaction):
        '''
            Validate a transaction and raise exception for invalid transaction.
            Validating transactions involves checking that the total currency
            sent to the recipient is correct, and that the signature itself is
            correct according to the public key and transaction output.
        '''
        # First check if transaction is actually a mining reward transaction.
        # If so, then validate that it is in the correct MINING REWARD format.
        # Else raise that it was an invalid reward.
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception('Invalid mining reward')
            return

        total_output = sum(transaction.output.values())
        if transaction.input['amount'] != total_output:
            raise Exception('Invalid transaction output values')
        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid Signature')

    @staticmethod
    def reward_transaction(miner_wallet):
        '''
            Generate a reward transaction that awards the miner.
        '''
        output = {}
        output[miner_wallet.address] = MINING_REWARD
        return Transaction(input=MINING_REWARD_INPUT, output=output)


def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction: {transaction.__dict__}')
    trans_json = transaction.to_json()
    restored_transaction = Transaction.from_json(trans_json)
    print(f'restored_transaction: {restored_transaction}')

if __name__ == '__main__':
    main()
