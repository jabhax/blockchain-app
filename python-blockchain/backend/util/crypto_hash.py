# crypto_hash.py

import hashlib
import json


def crypto_hash(*args):
    '''
        Returns a sha-256 hash of the given data.
        Implementation returns a hexdigest of encoded, stringified data.

        # NOTE:
        # str_args uses a mapping of args to a lambda function that simply
        # stringifies the jsonified args data. Lastly, it sorts it to preserve
        # the integrity of the hash.
    '''
    str_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(str_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")

if __name__ == '__main__':
    main()

