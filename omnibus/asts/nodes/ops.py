import ast  # noqa
import enum


class BinOp(enum.Enum):
    ADD = '+'
    BIT_AND = '&'
    BIT_OR = '|'
    BIT_XOR = '^'
    DIV = '/'
    FLOOR_DIV = '//'
    L_SHIFT = '<<'
    MAT_MULT = '*'
    MOD = '%'
    MULT = '*'
    POW = '**'
    R_SHIFT = '>>'
    SUB = '-'


class BoolOp(enum.Enum):
    AND = 'and'
    OR = 'or'


class CmpOp(enum.Enum):
    EQ = '=='
    GT = '>'
    GTE = '>='
    IN = 'in'
    IS = 'is'
    IS_NOT = 'is not'
    LT = '<'
    LTE = '<='
    NOT_EQ = '!='
    NOT_IN = 'not in'


class UnaryOp(enum.Enum):
    INVERT = '~'
    NOT = 'not'
    ADD = '+'
    SUB = '-'
