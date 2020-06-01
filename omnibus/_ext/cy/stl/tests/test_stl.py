from .. import stl as stl_


def test_vector():
    v = stl_.Int32Vector()
    v.append(2)
    v.append(3)
    v.append(1)
    for i in v:
        print(i)


def test_map():
    m = stl_.Int32Int32Map()
    m[2] = 20
    m[3] = 30
    m[1] = 10
    for k, v in m.items():
        print((k, v))


def test_bytes_vector():
    v = stl_.BytesVector()
    v.append(b'abc')
    v.append(b'def')
    for i in v:
        print(i)
