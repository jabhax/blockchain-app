# hex_to_binary.py

from backend.util.crypto_hash import crypto_hash


HEX_TO_BINARY_CONVERSION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}


def hex_to_binary(hex_str):
    binary_str = ''
    binary_str = ''.join(HEX_TO_BINARY_CONVERSION_TABLE[c] for c in hex_str)
    return binary_str

def main():
    num = 451

    # Convert test number to hexadecimal format.
    hex_num = hex(num)[2:]
    print(f'hex_num: {hex_num}')

    # Convert hexadecimal number to binary format.
    bin_num = hex_to_binary(hex_num)
    print(f'bin_num: {bin_num}')

    # Convert binary into format of original number.
    orig_num = int(bin_num, 2)
    print(f'orig_num: {orig_num}')

    # Call hex_to_binary on a crypto_hash output to validate that it works
    # for sha256.
    hex_to_bin_hash = hex_to_binary(crypto_hash('test-data'))
    print(f'hex_to_bin_hash: {hex_to_bin_hash}')


if __name__ == '__main__':
    main()
