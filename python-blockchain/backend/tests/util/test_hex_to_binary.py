# hex_to_binary.py

from backend.util.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    orig_num = 1234567890
    hex_num = hex(orig_num)[2:]
    bin_num = hex_to_binary(hex_num)
    # Assert that the binary returned from hex_to_binary is indeed the correct
    # representation for the original number.
    assert(int(bin_num, 2) == orig_num)


