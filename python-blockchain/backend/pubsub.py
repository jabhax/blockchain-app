import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-6a1ef7a8-d763-11ea-b3f2-c27cb65b13f4'
pnconfig.publish_key = 'pub-c-3f6cf192-f4d6-460a-90d0-8665abc15464'

CHANNELS = {
    'TEST': 'TEST_CHANNEL',
    'BLOCK': 'BLOCK_CHANNEL',
    'TRANSACTION': 'TRANSACTION_CHANNEL'
}

class Listener(SubscribeCallback):
    ''' Listener class for pubnub subscribing '''

    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, msg_obj):
        print(f'\n-- Channel: {msg_obj.channel}\n-- Message: {msg_obj.message}')

        if msg_obj.channel == CHANNELS['BLOCK']:
            block = Block.from_json(msg_obj.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_bc_transactions(self.blockchain)
                print(f'\n -- Successfully replaced the local chain.')
            except Exception as e:
                print(f'\n -- Could not replace the chain: {e}.')
        elif msg_obj.channel == CHANNELS['TRANSACTION']:
            trans = Transaction.from_json(msg_obj.message)
            self.transaction_pool.set_transaction(trans)
            print(f'\n -- Set the new transaction in the transaction pool')


class PubSub():
    '''
        Publish-Subscribe layer of the application.
        Provides communication between the nodes of the blockchain network.
    '''

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, ch, msg):
        ''' Publishes a message on the given channel using sync '''
        self.pubnub.publish().channel(ch).message(msg).sync()

    def broadcast_block(self, block):
        ''' Broadcast (publish) a block object to all nodes. '''
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, trans):
        ''' Broadcast (publish) a transaction objet to all nodes. '''
        self.publish(CHANNELS['TRANSACTION'], trans.to_json())


def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})


if __name__ == '__main__':
    main()
