# test_block.py

import pytest
import time

from backend.blockchain.block import Block, GEN_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary


def test_mine_block():
    '''
        Purpose:
            Test that a block can be mined.
            - Assert that genesis object is of type Block.
            - Assert that the currently mined block data is correct.
            - Assert that the last_block's hash matches the current block's
              last_hash.
    '''
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)
    # Assert that genesis object is of type Block.
    assert(isinstance(block, Block))
    # Assert that the currently mined block data is correct.
    assert(block.data == data)
    # Assert that the last_block's hash matches the current block's last_hash.
    assert(block.last_hash == last_block.hash)
    assert(hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty)

def test_genesis():
    '''
        Purpose:
            Test the integrity of the genesis block.
            - Assert that genesis object is of type Block.
            - Assert all genesis attributes and values with GEN_DATA attributes
              and values.
    '''
    genesis = Block.genesis()
    # Assert that genesis object is of type Block.
    assert(isinstance(genesis, Block))
    # Assert all genesis attributes and values with GEN_DATA attributes and values.
    for k, v in GEN_DATA.items():
        getattr(genesis, k) == v

def test_quickly_mined_block():
    '''
        Purpose:
            Test that the difficulty to mine a block increases when a block is
            mined to quickly.
    '''
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')
    # Assert that difficulty INCREASES by 1 when a block is mined too quickly.
    assert(mined_block.difficulty == last_block.difficulty + 1)

def test_slowly_mined_block():
    '''
        Purpose:
            Test that the difficulty to mine a block decreases when a block is
            mined too slowly.
    '''
    last_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')
    # Assert that difficulty DECREASES by 1 when a block is mined too slowly.
    assert(mined_block.difficulty == last_block.difficulty - 1)

def test_mined_block_diffculty_lower_bound_limit():
    '''
        Purpose:
            Test that the difficulty to mine a block will never fall below its
            lower bound.
    '''
    last_block = Block(time.time_ns(), 'test_last_hash', 'test_hash', 'test_data', 0, 1)
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')
    # Assert that difficulty is lower-bounded at 1 when a block's difficulty
    # attempts to decrease below 1 after being mined too quickly.
    assert(mined_block.difficulty == 1)

@pytest.fixture
def last_block():
    ''' Pytest Fixture for getting the genesis block '''
    return Block.genesis()

@pytest.fixture
def block(last_block):
    ''' Pytest Fixture for getting a mined test-block '''
    return Block.mine_block(last_block, 'test-data')

def test_valid_block(last_block, block):
    '''
        Purpose:
            Test that a block is valid.
    '''
    Block.is_valid(last_block, block)

def test_invalid_block(last_block, block):
    '''
        Purpose:
            Test that a block is invalid by corrupting its last_hash value and
            then validating.
    '''
    block.last_hash = 'test-bad-hash'
    with pytest.raises(Exception, match="must have a proper last_hash reference."):
        Block.is_valid(last_block, block)

def test_valid_block_invalid_proof_of_work(last_block, block):
    '''
        Purpose:
            Test that a block is not valid if the Proof-of-Work requirement is
            not met. Invalidate the Proof-of-Work by corrupting the block's
            hash value.
    '''
    block.hash = 'fff'
    with pytest.raises(Exception, match='did not meet the Proof of Work Requirement.'):
        Block.is_valid(last_block, block)

def test_valid_block_jumped_difficulty(last_block, block):
    '''
        Purpose:
            Test that the a valid block cannot adjust its diffuclty any more or
            less than 1. Set block difficulty to greater than 1 and validate.
    '''
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}111abc'
    with pytest.raises(Exception, match='difficulty must only adjust by 1.'):
        Block.is_valid(last_block, block)

def test_valid_block_invalid_hash(last_block, block):
    '''
        Purpose:
            Test that the block must have a valid hash. Corrupt the block's
            hash and validate.
    '''
    block.hash = '0000000000000000bbbabc'
    with pytest.raises(Exception, match='must have a proper hash reference.'):
        Block.is_valid(last_block, block)
