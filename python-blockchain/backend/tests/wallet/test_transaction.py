import pytest

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    trans = Transaction(sender_wallet, recipient, amount)
    # Assert that transaction amount of recipient is equal to the true amount
    assert(trans.output[recipient] == amount)
    # Assert that the change in the transaction amount is valid.
    trans_delta = sender_wallet.balance - amount 
    assert(trans.output[sender_wallet.address] == trans_delta)
    # Assert that the timestamp exists in the transaction input to verify that
    # it is a valide transaction.
    assert('timestamp' in trans.input)
    # Assert that the transaction input's amount is equal the wallet's balance.
    assert(trans.input['amount'] == sender_wallet.balance)
    # Assert that the transaction input's address is the true wallet address.
    assert(trans.input['address'] == sender_wallet.address)
    # Assert that the transaction input's public key is the true public key
    # of the wallet.
    assert(trans.input['public_key'] == sender_wallet.public_key)
    # At this point, all data seems to be correct. Run transaction through the
    # Wallet.verify() to verify the signature and assert that it is verified.
    assert(Wallet.verify(trans.input['public_key'], trans.output,
           trans.input['signature']))

def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds recipient balance'):
        Transaction(Wallet(), 'recipient', 9001)

def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    trans = Transaction(sender_wallet, 'recipient', 50)
    with pytest.raises(Exception, match='Amount exceeds the amount provided'):
        trans.update(sender_wallet, 'new_recipient', 9001)

def test_transaction_update():
    # Block Wallet that will be subtracting amounts from.
    sender_wallet = Wallet()

    # Set the first recipient, the first amount that will be subtracted from
    # the Block's wallet, and the transaction item that will be used in the
    # process.
    recipient1 = 'first_recipient'
    amount1 = 50
    trans = Transaction(sender_wallet, recipient1, amount1)

    # Set the second recipient, the second amount that will be subtracted from
    # the Block's wallet, and the transaction item that will be used in the
    # process.
    recipient2 = 'next_recipient'
    amount2 = 75
    trans.update(sender_wallet, recipient2, amount2)

    # Assert that the transaction output for the recipient2 is amount2.
    assert(trans.output[recipient2] == amount2)
    # Assert that the sender wallet in the output is updated.
    updated_balance = sender_wallet.balance - amount1 - amount2
    assert(trans.output[sender_wallet.address] == updated_balance)
    # Run transaction through the Wallet.verify() to verify the signature and
    # assert that it is verified.
    assert(Wallet.verify(trans.input['public_key'], trans.output,
           trans.input['signature']))

    # Make an update to the first recipient using the wallet and new third
    # amount.
    amount3 = 25
    trans.update(sender_wallet, recipient1, amount3)

    # Assert that the total amount recieved by recipient1 during the
    # transactions are the sum total of amount1 + amount3.
    total_amount_added = amount1 + amount3
    assert(trans.output[recipient1] == total_amount_added)

    # Assert amount1, amount2, and amount3 was subtracted from wallet.
    total_update_change = (sender_wallet.balance - amount1 - amount2 - amount3)
    assert(trans.output[sender_wallet.address] == total_update_change)

    # Run transaction through the Wallet.verify() to verify the signature and
    # assert that it is verified.
    assert(Wallet.verify(trans.input['public_key'], trans.output,
           trans.input['signature']))

def test_valid_transaction():
    Transaction.is_valid(Transaction(Wallet(), 'recipient', 50))

def test_valid_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    trans = Transaction(sender_wallet, 'recipient', 50)
    trans.output[sender_wallet.address] = 9001
    with pytest.raises(Exception, match='Invalid transaction output values'):
        Transaction.is_valid(trans)

def test_valid_transaction_with_invalid_signature():
    trans = Transaction(Wallet(), 'recipient', 50)
    # Try to update the signature with a new signature that uses a new signed
    # version of the valid transaction output data.
    trans.input['signature'] = Wallet().sign(trans.output)
    with pytest.raises(Exception, match='Invalid Signature'):
        Transaction.is_valid(trans)
