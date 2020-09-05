import itertools

import pytest

from .. import ents as ents_  # noqa
from .. import gens as gens_  # noqa
from .. import rand as rand_  # noqa
from .. import text as text_  # noqa


@pytest.mark.xfail()
def test_tpch():
    exp = [
        ents_.Customer(
            row_number=1,
            customer_key=1,
            name="Customer#000000001",
            address="IVhzIApeRb ot,c,E",
            nation_key=15,
            phone="25-989-741-2988",
            account_balance=71156,
            market_segment="BUILDING",
            comment="to the even, regular platelets. regular, ironic epitaphs nag e",
        ),
        ents_.Customer(
            row_number=2,
            customer_key=2,
            name="Customer#000000002",
            address="XSTf4,NCwDVaWNe6tEgvwfmRchLXak",
            nation_key=13,
            phone="23-768-687-3665",
            account_balance=12165,
            market_segment="AUTOMOBILE",
            comment="l accounts. blithely ironic theodolites integrate boldly: caref",
        ),
    ]

    cg = gens_.CustomerGenerator(10, 1, 20)
    got = list(itertools.islice(cg, 2))
    assert got == exp

    cg = gens_.CustomerGenerator(10, 1, 20)
    for c in cg:  # noqa
        pass
