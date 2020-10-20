from .. import parsing


def test_minml():
    print(parsing.parse('{"hi": 1}'))

    for s in [
        '1',
        '0x1a',
        'ab-c',
        'a0_c',
        '-4.20e8',
        '"a": null',
        '"b": null, \n "c": 420',
        '{"b": null, "c": 420}',
        '{a: b}',
        '{a: b,}',
        '{a: b, c}',
        '{}',
        '[]',
        '[a, """hi\nthere""", 5]',
        "{0: 'a'}",
        "{a$b.c: 420}",
        "{a$b.c}",
    ]:
        if not s.startswith('{') and s.startswith('}'):
            s = '{' + s + '}'
        print(repr(parsing.parse(s)))
