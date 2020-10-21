from .. import scan


def test_scan():
    m = scan.Scanner('{} x {asdf:}').scan('ab x cd')
    print(m)

    assert scan.Scanner('a {v:x}').scan('a abc')['v'] == 0xabc

    # s = scan.Scanner('ab{{{cd}}}ef{gh}ij')
    print(scan.Scanner('ab {} cd').scan('ab x cd'))
    print(scan.Scanner('{} x {:}').scan('ab x cd'))
    print(scan.Scanner('ab {x} cd').scan('ab x cd'))
    print(scan.Scanner('ab {x:} cd').scan('ab x cd'))
    print(scan.Scanner('ab {x:d} cd').scan('ab 82 cd'))
