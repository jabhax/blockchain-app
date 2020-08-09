import os
import requests
import random

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route('/')
def index():
    ''' index/home endpoint for blockchain '''
    return 'Horray! Welcome to the blockchain!'

@app.route('/blockchain')
def route_blockchain():
    ''' Endpoint for viewing the blockchain '''
    return jsonify(blockchain.to_json())

@app.route('/blockchain/range')
def route_blockchain_range():
    ''' Endpoint for viewing paginated blockchain '''
    # http://localhost:5000/blockchain/range?start=2&end=5
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    # blockchain.to_json()[::-1] reverses the list. [start:end] gets the
    # blockchain from start to end on the reversed list.
    return jsonify(blockchain.to_json()[::-1][start:end])

@app.route('/blockchain/length')
def route_blockchain_length():
    '''
        Endpoint for viewing the length of the blockchain
        (how many blocks in the chain).
    '''
    return jsonify(len(blockchain.chain))

@app.route('/blockchain/mine')
def route_blockchain_mine():
    ''' Endpoint for mining a block '''
    trans_data = transaction_pool.transaction_data()
    trans_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(trans_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_bc_transactions(blockchain)
    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    ''' Endpoint for transacting a wallet '''
    trans_data = request.get_json()
    trans = transaction_pool.existing_transaction(wallet.address)
    if trans:
        trans.update(wallet, trans_data['recipient'], trans_data['amount'])
    else:
        trans = Transaction(wallet, trans_data['recipient'], trans_data['amount'])
    pubsub.broadcast_transaction(trans)
    return jsonify(trans.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address': wallet.address, 'balance': wallet.balance })


ROOT_PORT = 5000
PORT = ROOT_PORT
BLOCKCHAIN_URL = f'http://localhost:{ROOT_PORT}/blockchain'

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    result = requests.get(BLOCKCHAIN_URL)
    result_blockchain = Blockchain.from_json(result.json())
    # This handles synchronizing the local chain to the true blockchain through
    # chain replacement.
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- Successfully synchronized the local chain.')
    except Exception as e:
        print(f'\n -- Error synchronizing: {e}')

if os.environ.get('SEED_DATA') == 'True':
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json(),
            Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json()
        ])

app.run(port=PORT)
