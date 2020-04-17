from .. import math as math_


def test_bits():
    assert math_.get_bit(3, 0b0100) == 0
    assert math_.get_bit(2, 0b0100) == 1
    assert math_.get_bits(1, 2, 0b0100) == 0b10
    assert math_.get_bits(1, 3, 0b0100) == 0b10
    assert math_.get_bits(0, 3, 0b0100) == 0b100
    assert math_.get_bits(1, 1, 0b0100) == 0
    assert math_.set_bit(2, 1, 0b01010) == 0b01110
    assert math_.set_bit(3, 0, 0b01010) == 0b00010
    assert math_.set_bits(1, 2, 0b11, 0b01010) == 0b01110
    assert math_.set_bits(1, 2, 0b10, 0b01010) == 0b01100
