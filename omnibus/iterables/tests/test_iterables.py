from .. import transforms as transforms_
from ... import code


class SomeType:
    pass


def test_dict():
    class Thing(transforms_.IterableTransform):
        def __call__(self):
            pass
    Thing().__dict__


def test_compose():
    @code.alias()
    def inc(x):
        return x + 1

    @code.alias()
    def dbl(x):
        return x * 2
    f = transforms_.compose(inc, dbl)
    assert isinstance(f, transforms_.IterableTransform)
    assert 'compose(children=(inc, dbl))' == repr(f)
    assert 10 == f(4)


def test_map():
    f = transforms_.compose(transforms_.map(lambda x: x + 1), transforms_.eager)
    assert list(range(1, 5)) == f(range(4))


def test_base():
    @transforms_.alias(SomeType)
    def dbl(xs):
        for x in xs:
            yield x * 2
    assert [0, 2, 4, 6] == list(dbl(range(4)))
    assert isinstance(dbl, SomeType)


def test_route():
    def add_100(ys):
        return list(map(lambda y: y + 100, ys))

    def route(x):
        return add_100 if 3 < x < 7 else None

    assert \
        [
            [
                0,
                1,
                2,
                3,
            ],
            [
                104,
                105,
                106,
            ],
            [
                7,
                8,
                9,
            ],
        ] == list(
            map(
                list,
                transforms_.route(route)(range(10))
            )
        )


def test_chunk():
    assert \
        [
            [
                0,
                1,
                2,
            ],
            [
                3,
                4,
                5,
            ],
            [
                6,
                7,
            ],
        ] == list(
            transforms_.chunk(3)(range(8))
        )


def test_match():
    assert \
        [
            [
                0,
                1,
                2,
                3,
                4,
                5,
            ],
            [
                16,
                17,
                18,
                19,
                20,
            ],
            [
                111,
                112,
                113,
                114,
            ],
        ] == list(
            map(
                list,
                transforms_.match(
                    lambda x: x > 10, lambda xs: list(map(lambda x: x + 100, xs)),
                    lambda x: x > 5, lambda xs: list(map(lambda x: x + 10, xs))
                )(range(15))
            )
        )

    assert \
        [
            [
                10,
                11,
            ],
            [
                '102',
                '103',
            ],
            [
                14,
            ]
        ] == list(
            map(
                list,
                transforms_.match(
                    lambda x: x in [2, 3], lambda xs: ['10' + str(x) for x in xs],
                    lambda x: True, lambda xs: [x + 10 for x in xs],
                )(range(5))
            )
        )


def test_type_match():
    assert \
        [
            [
                '2*10',
            ],
            [
                2,
                4.0,
            ],
            [
                '2*3',
            ],
            [
                10,
            ],
        ] == list(
            map(
                list,
                transforms_.type_match(
                    (int, float), lambda xs: list(map(lambda x: x * 2, xs)),
                    str, lambda xs: list(map(lambda x: '2*' + x, xs))
                )([
                    '10',
                    1,
                    2.0,
                    '3',
                    5,
                ])
            )
        )


def test_type_match_sorted():
    assert \
        [
            [
                2,
                4.0,
                10,
            ],
            [
                '2*10',
                '2*3',
            ],
        ] == list(
            map(
                list,
                transforms_.type_match(
                    (int, float), lambda xs: list(map(lambda x: x * 2, xs)),
                    str, lambda xs: list(map(lambda x: '2*' + x, xs)),
                    sorted=True
                )([
                    '10',
                    1,
                    2.0,
                    '3',
                    5,
                ])
            )
        )

    assert \
        [
            [
                2,
                4.0,
                10,
            ],
            [
                '2*10',
                '2*3',
            ],
        ] == list(
            map(
                list,
                transforms_.type_match(
                    (int, float), lambda xs: list(map(lambda x: x * 2, xs)),
                    str, lambda xs: list(map(lambda x: '2*' + x, xs)),
                    sorted=True
                )([
                    1,
                    '10',
                    2.0,
                    '3',
                    5,
                ])
            )
        )


def test_deduplicate():
    assert \
        [
            1,
            2,
            3,
            4,
            5,
        ] == list(
            transforms_.deduplicate()([
                1,
                2,
                1,
                3,
                3,
                4,
                1,
                5,
                5,
                1,
                2,
            ])
        )

    assert \
        [
            'abc',
            'ade',
            'afg',
            'bhi',
        ] == list(
            transforms_.deduplicate(keys=tuple)([
                'abc',
                'abc',
                'ade',
                'abc',
                'afg',
                'ade',
                'bhi',
            ])
        )

    assert \
        [
            transforms_.Deduplicated(*t) for t in [
                (
                    1,
                    0,
                    1,
                    (1,),
                    (1,),
                ),
                (
                    2,
                    0,
                    2,
                    (2,),
                    (2,),
                ),
                (
                    2,
                    1,
                    1,
                    (1,),
                    (),
                ),
                (
                    3,
                    1,
                    3,
                    (3,),
                    (3,),
                ),
                (
                    3,
                    2,
                    2,
                    (2,),
                    (),
                ),
            ]
        ] == list(
            transforms_.deduplicate(verbose=True)([
                1,
                2,
                1,
                3,
                2,
            ])
        )


def test_operators():
    assert (+(transforms_.nop * (lambda x: x + 1)))(range(3)) == [1, 2, 3]
    assert (+(transforms_.nop * (lambda x: x + 1) @ (lambda x: x % 2 == 0)))(range(6)) == [2, 4, 6]


def test_multi_combinations():
    assert list(transforms_.multi_combinations('abc', 'def', 'ghi')) == [
        ['a', 'd', 'g'],
        ['a', 'd', 'h'],
        ['a', 'd', 'i'],
        ['a', 'e', 'g'],
        ['a', 'e', 'h'],
        ['a', 'e', 'i'],
        ['a', 'f', 'g'],
        ['a', 'f', 'h'],
        ['a', 'f', 'i'],

        ['b', 'd', 'g'],
        ['b', 'd', 'h'],
        ['b', 'd', 'i'],
        ['b', 'e', 'g'],
        ['b', 'e', 'h'],
        ['b', 'e', 'i'],
        ['b', 'f', 'g'],
        ['b', 'f', 'h'],
        ['b', 'f', 'i'],

        ['c', 'd', 'g'],
        ['c', 'd', 'h'],
        ['c', 'd', 'i'],
        ['c', 'e', 'g'],
        ['c', 'e', 'h'],
        ['c', 'e', 'i'],
        ['c', 'f', 'g'],
        ['c', 'f', 'h'],
        ['c', 'f', 'i'],
    ]
