from backend.wallet.wallet import Wallet


def test_veirfy_valid_signature():
    ''' Test that a wallet can verify a valid signature correctly '''
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert(Wallet.verify(wallet.public_key, data, signature))

def test_veirfy_invalid_signature():
    ''' Test that a wallet can verify & deny an invalid signature correctly '''
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert(not(Wallet.verify(Wallet().public_key, data, signature)))

