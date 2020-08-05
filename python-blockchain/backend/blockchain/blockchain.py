# blockchain.py

from backend.blockchain.block import Block


class Blockchain:
    '''
        Blockchain: a public ledger of transactions.
        Implemented as a list of Blocks, which are datasets of transactions.
    '''
    def __init__(self):
        ''' Blockchain constructor '''
        self.chain = [Block.genesis()]

    def add_block(self, data):
        ''' Appends a block to the chain '''
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        '''
            Replace the local chain with incoming chain if ALL below applies:
                - The incoming chain is longer than the local chain.
                - The incoming chain is formatted properly.
        '''
        if len(self.chain) >= len(chain):
            raise Exception('Cannot replace. Incoming chain must be longer than local.')

        try:
            Blockchain.is_valid(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')
        self.chain = chain

    def to_json(self):
        ''' Serialize the blockchain into a list of blocks. '''
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def is_valid(chain):
        '''
            Validate a block-chain by enforcing the following rules:
                - The chain must start with the genesis block.
                - Each block in the chain must be formatted correctly.
        '''
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid.')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid(last_block, block)


def main():
    blockchain = Blockchain()
    blockchain.add_block('second_blk')
    blockchain.add_block('third_blk')

    print(blockchain)
    print(f'blockchain.py ___name__: {__name__}')


if __name__ == '__main__':
    main()
