from .. import scan


def test_scan():
    m = scan.Scanner('{} x {asdf:}').scan('ab x cd')
    print(m)

    assert scan.Scanner('a {v:x}').scan('a abc')['v'] == 0xabc

    # s = scan.Scanner('ab{{{cd}}}ef{gh}ij')
    print(scan.scan('ab {} cd', 'ab x cd'))
    print(scan.scan('{} x {:}', 'ab x cd'))
    print(scan.scan('ab {x} cd', 'ab x cd'))
    print(scan.scan('ab {x:} cd', 'ab x cd'))
    print(scan.scan('ab {x:d} cd', 'ab 82 cd'))

    assert list(scan.scan('{:w} {^:w}', 'x    y').values) == ['x', 'y']
    assert scan.scan('{:w} {:w}', 'x   y') is None

    scan.Scanner(r'{:r\w}')
