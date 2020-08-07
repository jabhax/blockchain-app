
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_set_transaction():
    trans_pool = TransactionPool()
    trans = Transaction(Wallet(), 'recipient', 1)
    trans_pool.set_transaction(trans)
    assert(trans_pool.transaction_map[trans.id] == trans)
