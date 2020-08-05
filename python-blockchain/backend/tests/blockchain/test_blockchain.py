# test_blockchain.py

import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GEN_DATA



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
        blockchain.add_block(i)
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
