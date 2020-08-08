# blockchain.py

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT


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
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. Incoming chain must be longer than local.')

        try:
            Blockchain.is_valid(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')
        self.chain = chain

    def to_json(self):
        ''' Serialize the blockchain into a list of blocks. '''
        return list(map(lambda b: b.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        '''
        De-serializes a list of serialized blocks into a Blockchain instance.
        '''
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda b: Block.from_json(b), chain_json))
        return blockchain

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
        Blockchain.is_valid_trans_chain(chain)

    def is_valid_trans_chain(chain):
        '''
            Enforce the rules of a chain composed of blocks of transaction.
                - Each transaction must only appear ONCE in the chain.
                - There can only be ONE mining reward per block.
                - Each transaction MUST be valid.
        '''
        trans_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for trans_json in block.data:
                trans = Transaction.from_json(trans_json)

                if trans.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception('There can only be one mining reward '
                                        'per block. Check block with hash: '
                                        f'{block.hash}')
                    has_mining_reward = True
                else:
                    if trans.id in trans_ids:
                        raise Exception(f'Transaction {trans.id} is not unique.')

                    trans_ids.add(trans.id)
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain, trans.input['address'])
                    if historic_balance != trans.input['amount']:
                        raise Exception(
                            f'Transaction {trans.id} has an invalid input amount.')
                    Transaction.is_valid(trans)


def main():
    blockchain = Blockchain()
    blockchain.add_block('second_blk')
    blockchain.add_block('third_blk')

    print(blockchain)
    print(f'blockchain.py ___name__: {__name__}')


if __name__ == '__main__':
    main()
