from .. import chd as chd_


def test_fnv():
    assert chd_.fnv1a_64(b'Hello') == 0x63f0bfacf2c00f6b


def test_fnv_fallback():
    assert chd_._fnv1a_64(b'Hello') == 0x63f0bfacf2c00f6b


GO_ZERO_SEED_RAND_U64S = [
    0xf1f85ff53eb60825,
    0xa7ecbff20de97a55,
    0x5e1a31f64a1b63c1,
    0x3143a81fa7c3d90b,
    0xe5acea102ad7bda1,
    0x49e0bfd0e7111c77,
    0xd98b335645e66538,
    0x9becadf140ef999c,
    0xc64fbd7f04799e85,
    0xc97dadc5cca510bd,
    0x5b3d97166d1aec28,
    0x829f3dd43d8cf1f9,
    0x358e4103b16d09d4,
    0x66e2c7c048ea3ba1,
    0xaef3141e70027058,
    0x1aa0b75b50e34fc9,
    0x26bb2d83bb3938f8,
    0x506d442d5e545ba3,
    0xa5d214515c11955d,
    0x8ad50cfb04a6a0e4,
    0x84a2a29f1d688138,
    0xc1883f289a45a6d5,
    0xd9c37ebe156ada0e,
    0xec55a668f103a3d1,
    0x789f21fdd5b37852,
    0x0ac8085cd1e1e761,
    0x6de46015f714ce60,
    0x086993c7cbb0cd88,
    0x95ac0d32d9d3152c,
    0x0b49ccb984022b11,
    0xa205d6cc8374d8f7,
    0x3ed8d17a1d759074,
    0xc906d1fdd643e3c7,
    0x7228104f4a22cfa1,
    0x6164aef2edbf1062,
    0x7eb304df214058ad,
    0xc2b053286e920cce,
    0x3ace634547cdbf4b,
    0xeba1159335d00278,
    0xe0bccd5ecfa80696,
    0xa81b15fddf9ea08d,
    0x77971649d4b6d816,
    0xc5f42589e06f9e62,
    0x00fcfb74ed9292e4,
    0x37b40d89e41b756d,
    0x76207ca94a76c190,
    0x777974e0601c3389,
    0xa3d5a2d1fa62cd44,
    0x640aac43395933a9,
    0x5c7a50241515532a,
    0x42d9c797993e814b,
    0x9b5507bbb8a0175a,
    0xeb6d202cda3c48ef,
    0x79e15eefac84b8cd,
    0x06b3d5b4ce90a52c,
    0x94e84939dc877384,
    0x3570cd38042c3c1e,
    0x8a7f1b0e4dce89c7,
    0x1a61001eb27eca21,
    0x35c3ee40b74ed782,
    0x32f9d066d148e308,
    0xd40230cd5a0028d9,
    0xb50343ef0c0e9952,
    0x347c5ffe2d2b3d5b,
    0xe3b988e975855c03,
    0xebdd64ec936f835f,
    0x6e1cbd172eae72d9,
    0x1ef8211d48fea558,
    0xe8ecc10fbf0996d2,
    0xa70e6d34388df634,
    0xb17aa25dfc7a0572,
    0x8b8435334b76c9fe,
    0x40c14ea2ff7f309b,
    0x0548ff81cf92b873,
    0x75a56a8d0f2053d6,
    0x85a3a57f8a174671,
    0xf882b72c7e061afd,
    0x9367bc5625d8dbf5,
    0xe5cabf441c146413,
    0xf34195d483b9af3f,
    0xdc6e1928045f3d89,
    0x4f977aedd05bfa1c,
    0x1a72bebdf53e7486,
    0x6b8a5578683fc413,
    0x65a1401334b54c58,
    0x1d7cfb0c5c322d13,
    0x756dc2b9ab23db94,
    0xa7025b99dcbf6aac,
    0x3db8b4edf8a47b73,
    0xbeaf4ed37a20c367,
    0xecd12c783bb90ea6,
    0x5de71a8b0929de6a,
    0x8a5b1d80d5561413,
    0x89f3187d6c838e08,
    0x263a804c49ae097a,
    0x76e0a957f9baf398,
    0xe5969cad485a3f89,
    0xde246f499662ccef,
    0xdb44234881e7683f,
    0xb36d1d2da296970c,
]


def test_chd():
    sample_data = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
    }

    c = chd_.ChdBuilder(
        {k.encode('utf8'): v.encode('utf8') for k, v in sample_data.items()},
        rand_u64=iter(GO_ZERO_SEED_RAND_U64S).__next__,
    ).chd

    assert c == chd_.Chd(
        r=[
            0xf1f85ff53eb60825,
            0x5e1a31f64a1b63c1,
            0xd98b335645e66538,
        ],
        indices=[1, 2, 0],
        keys=[
            b'six',
            b'two',
            b'one',
            b'five',
            b'four',
            b'three',
            b'seven',
        ],
        values=[
            b'6',
            b'2',
            b'1',
            b'5',
            b'4',
            b'3',
            b'7',
        ],
    )

    assert len(c.keys) == 7

    for k, v in sample_data.items():
        assert c.get(k.encode('utf8')) == v.encode('utf8')

    assert c.get('monkey'.encode('utf8')) is None
