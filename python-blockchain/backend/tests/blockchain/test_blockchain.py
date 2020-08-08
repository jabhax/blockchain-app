# test_blockchain.py

import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GEN_DATA
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction


def test_blockchain_instance():
    '''
        Purpose:
            Assert that the blockchain's first block is the gensis block
            instance.
    '''
    blockchain = Blockchain()
    assert(blockchain.chain[0].hash == GEN_DATA['hash'])

def test_add_block():
    '''
        Purpose:
            Assert that the blockchain added the block and that the data
            matches.
    '''
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)
    assert(blockchain.chain[-1].data == data)

@pytest.fixture
def blockchain_3b():
    ''' Pytest Fixture for a blockchain containing 3 blocks '''
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain

def test_valid_chain(blockchain_3b):
    '''
        Purpose:
            Test whether a given blockchain is valid.
    '''
    Blockchain.is_valid(blockchain_3b.chain)

def test_invalid_chain(blockchain_3b):
    '''
        Purpose:
            Test whether a given blockchain is invalid by corrupting it's
            genesis block and performing validation.
    '''
    blockchain_3b.chain[0].hash = 'test-bad-hash'
    with pytest.raises(Exception, match='genesis block must be valid.'):
        Blockchain.is_valid(blockchain_3b.chain)

def test_replace_chain(blockchain_3b):
    '''
        Purpose:
            Test whether a given blockchain can perform Chain Replacement.
            Assert that chain replacement can be done if the replacement-chain
            is longer than the replaced-chain and is formatted correctly.
    '''
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_3b.chain)
    assert(blockchain.chain == blockchain_3b.chain)

def test_replace_chain_short_chain(blockchain_3b):
    '''
        Purpose:
            Test whether a given blockchain can perform Chain Replacement.
            Assert that chain replacement can NOT be done if the
            replacement-chain is shorter or equal to the replaced-chain.
    '''
    blockchain = Blockchain()
    with pytest.raises(Exception, match='Incoming chain must be longer than local'):
        blockchain_3b.replace_chain(blockchain.chain)

def test_replace_chain_invalid_chain(blockchain_3b):
    '''
        Purpose:
            Test whether a given blockchain can perform Chain Replacement.
            Assert that chain replacement can not be done if the
            replacement-chain is invalid.
    '''
    blockchain = Blockchain()
    blockchain_3b.chain[1].hash = 'test-bad-hash'
    with pytest.raises(Exception, match='incoming chain is invalid'):
        blockchain.replace_chain(blockchain_3b.chain)

def test_valid_transaction_chain(blockchain_3b):
    Blockchain.is_valid_trans_chain(blockchain_3b.chain)

def test_is_valid_transaction_chain_duplicate_transactions(blockchain_3b):
    trans = Transaction(Wallet(), 'recipient', 1).to_json()
    # Add block with list of transactions containing two identical transactions
    # (a duplicate)
    blockchain_3b.add_block([trans, trans])
    with pytest.raises(Exception, match='is not unique.'):
        Blockchain.is_valid_trans_chain(blockchain_3b.chain)

def test_is_valid_transaction_chain_multiple_rewards(blockchain_3b):
    reward1 = Transaction.reward_transaction(Wallet()).to_json()
    reward2 = Transaction.reward_transaction(Wallet()).to_json()
    blockchain_3b.add_block([reward1, reward2])
    with pytest.raises(Exception, match='one mining reward per block.'):
        Blockchain.is_valid_trans_chain(blockchain_3b.chain)

def test_is_valid_transaction_chain_bad_transaction(blockchain_3b):
    bad_trans = Transaction(Wallet(), 'recipient', 1)
    bad_trans.input['signature'] = Wallet().sign(bad_trans.output)
    blockchain_3b.add_block([bad_trans.to_json()])
    with pytest.raises(Exception):
        Blockchain.is_valid_trans_chain(blockchain_3b.chain)

def test_is_valid_transaction_chain_bad_histroric_balance(blockchain_3b):
    wallet = Wallet()
    bad_trans = Transaction(wallet, 'recipient', 1)
    bad_trans.output[wallet.address] = 9001
    bad_trans.input['amount'] = 9002
    bad_trans.input['signature'] = wallet.sign(bad_trans.output)
    blockchain_3b.add_block([bad_trans.to_json()])
    with pytest.raises(Exception, match='has an invalid input amount.'):
        Blockchain.is_valid_trans_chain(blockchain_3b.chain)
