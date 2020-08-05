# block.py

import time

from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GEN_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'nonce': 'genesis_nonce',
    'difficulty': 3
}

class Block:
    ''' 
        Block: a unit of storage.
        Store transactions in a blockchain that supports a cryptocurrency.
    '''
    def __init__(self, timestamp, last_hash, hash, data, nonce, difficulty):
        '''
            Block object constructor.
            Args:
                timestamp - time in nanoseconds: the time that the block was created.
                last_hash - hash value: reference to hash of preceding block.
                hash - hash value: hash value of the data of the given block.
                data - data of the block:
                nonce - int: number of mined attempts for the proof of work
                             computation based on leading zero requirement.
                difficulty - int: difficulty based on leading zero requirement.
        '''
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.nonce = nonce
        self.difficulty = difficulty

    def __repr__(self):
        block_repr = (
            'Block(\n'
            f'timestamp: {self.timestamp}\n'
            f'last_hash: {self.last_hash}\n'
            f'hash: {self.hash}\n'
            f'data: {self.data}\n'
            f'nonce: {self.nonce}\n'
            f'difficulty: {self.difficulty})\n'
        )
        return block_repr

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        ''' Serialize a Block instance into a dictionary of its attributes '''
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        ''' 
            Mines a Block based on the given last_block and data arguments,
            until a block hash is found that meets the leading zero's
            Proof of Work requirements.
        '''
        timestamp = time.time_ns()
        last_hash = last_block.hash
        nonce = 0
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        hash = crypto_hash(timestamp, last_hash, data, nonce, difficulty)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, nonce, difficulty)

        block = Block(timestamp, last_hash, hash, data, nonce, difficulty)
        return block

    @staticmethod
    def genesis():
        ''' 
            Generate the Genesis Block.
            Returns Block (
                timestamp=GEN_DATA['timestamp'],
                last_hash=GEN_DATA['last_hash'],
                hash=GEN_DATA['hash'],
                data=GEN_DATA['data']),
                nonce=GEN_DATA['nonce']),
                difficulty=GEN_DATA['difficulty'])
        '''
        block = Block(**GEN_DATA)
        return block

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        '''
            Calculate the adjusted difficulty based on the MINE_RATE.
            Increase difficulty if blocks are mined too quickly.
            Decrease difficulty if blocks are mined too slowly.
        '''
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return int(last_block.difficulty + 1)

        if (last_block.difficulty - 1) > 0:
            return int(last_block.difficulty - 1)

        return 1

    def is_valid(last_block, block):
        '''
            Validate a block by enforcing the following rules:
                - The block must have the proper last_hash reference.
                - The block must meet the Proof-of-Work requirement.
                - The difficulty must only adjust by (+/-) 1.
                - The block hash must be a valid combination of the block fields.
        '''
        if block.last_hash != last_block.hash:
            raise Exception('The block must have a proper last_hash reference.')

        if hex_to_binary(block.hash)[0:block.difficulty] != ('0' * block.difficulty):
            raise Exception('The block did not meet the Proof of Work Requirement.')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must only adjust by 1.')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block must have a proper hash reference.')


def main():
    genesis_block = Block.genesis()
    good_block = Block.mine_block(Block.genesis(), 'foo')
    #good_block.last_hash = 'evil_hash'
    try:
        Block.is_valid(genesis_block, good_block)
    except Exception as e:
        print(f'Block.is_valid: {e}')


if __name__ == '__main__':
    main()
