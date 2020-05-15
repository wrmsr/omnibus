"""
TODO:
 - (|u)int(8|16|32|64)
  - + cython lol
"""
import typing as ta

from .classes import Final


def isclose(a: float, b: float, *, rel_tol: float = 1e-09, abs_tol: float = 0.0) -> float:
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def get_bit(bit: int, value: int) -> int:
    return (value >> bit) & 1


def get_bits(bits_from: int, num_bits: int, value: int) -> int:
    return (value & ((1 << (bits_from + num_bits)) - 1)) >> bits_from


def set_bit(bit: int, bit_value: ta.Union[bool, int], value: int) -> int:
    if bit_value:
        return value | (1 << bit)
    else:
        return value & ~(1 << bit)


def set_bits(bits_from: int, num_bits: int, bits_value: int, value: int) -> int:
    return value & ~(((1 << num_bits) - 1) << bits_from) | (bits_value << bits_from)


class Infinity(Final):

    def __repr__(self):
        return 'Infinity'

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Infinity)

    def __ne__(self, other):
        return not isinstance(other, Infinity)

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __neg__(self):
        return NEGATIVE_INFINITY


class NegativeInfinity(Final):

    def __repr__(self):
        return '-Infinity'

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, NegativeInfinity)

    def __ne__(self, other):
        return not isinstance(other, NegativeInfinity)

    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return False

    def __neg__(self):
        return INFINITY


INFINITY = Infinity()

NEGATIVE_INFINITY = NegativeInfinity()
