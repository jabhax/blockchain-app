from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE

def test_veirfy_valid_signature():
    ''' Test that a wallet can verify a valid signature correctly '''
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert(Wallet.verify(wallet.public_key, data, signature))

def test_veirfy_invalid_signature():
    ''' Test that a wallet can verify & deny an invalid signature correctly '''
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert(not(Wallet.verify(Wallet().public_key, data, signature)))

def test_calculate_balance():
    ''' Test that a wallet can calculate its balance correctly. '''
    blockchain = Blockchain()
    wallet = Wallet()

    # Assert that the wallet's balance on a new blockchain is equal to the
    # global starting balance.
    assert(Wallet.calculate_balance(
        blockchain, wallet.address) == STARTING_BALANCE)

    # Create a transaction of amount 50 and verify that it is subtracted from
    # the wallet's balance after adding the new transaction to the blockchain.
    amount = 50
    trans = Transaction(wallet, 'recipient', amount)
    blockchain.add_block([trans.to_json()])
    EXPECTED_BALANCE = STARTING_BALANCE - amount

    # Assert that the new calculated balance is equal to the expected balance.
    assert(Wallet.calculate_balance(
        blockchain, wallet.address) == EXPECTED_BALANCE)

    # Create first transaction to be recieved by the wallet after the calculation.
    recieved_amount1 = 25
    recieved_trans1 = Transaction(Wallet(), wallet.address, recieved_amount1)

    # Create second transaction to be recieved by the wallet after the calculation.
    recieved_amount2 = 43
    recieved_trans2 = Transaction(Wallet(), wallet.address, recieved_amount2)

    blockchain.add_block([recieved_trans1.to_json(), recieved_trans2.to_json()])
    EXPECTED_BALANCE = (STARTING_BALANCE - amount + recieved_amount1 +
                        recieved_amount2)

    # Assert that the new calculated balance is equal to the expected balance.
    assert(Wallet.calculate_balance(
        blockchain, wallet.address) == EXPECTED_BALANCE)
