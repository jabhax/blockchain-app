
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain

def test_set_transaction():
    trans_pool = TransactionPool()
    trans = Transaction(Wallet(), 'recipient', 1)
    trans_pool.set_transaction(trans)
    assert(trans_pool.transaction_map[trans.id] == trans)

def test_clear_blockchain_transactions():
    trans_pool = TransactionPool()
    trans1 = Transaction(Wallet(), 'recipient', 1)
    trans2 = Transaction(Wallet(), 'recipient', 2)
    trans_pool.set_transaction(trans1)
    trans_pool.set_transaction(trans2)

    blockchain = Blockchain()
    blockchain.add_block([trans1.to_json(), trans2.to_json()])
    # Assert that transaction 1 is in the transaction map of the pool.
    assert(trans1.id in trans_pool.transaction_map)
    # Assert that transaction 2 is in the transaction map of the pool.
    assert(trans2.id in trans_pool.transaction_map)
    trans_pool.clear_bc_transactions(blockchain)
    # Assert that transaction 1 is NOT in the transaction map of the pool.
    assert(not(trans1.id in trans_pool.transaction_map))
    # Assert that transaction 2 is NOT in the transaction map of the pool.
    assert(not(trans2.id in trans_pool.transaction_map))
