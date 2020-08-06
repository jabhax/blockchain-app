import os
import requests
import random

from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub



app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)

@app.route('/')
def index():
    ''' index/home endpoint for blockchain '''
    return 'Horray! Welcome to the blockchain!'

@app.route('/blockchain')
def route_blockchain():
    ''' Endpoint for viewing the blockchain '''
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    ''' Endpoint for mining a block '''
    transaction_data = 'stubbed_transaction_data'
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json())


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

app.run(port=PORT)
