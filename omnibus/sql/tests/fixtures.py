import typing as ta

import pytest
import sqlalchemy as sa
import sqlalchemy.pool

from ... import lang


@pytest.fixture()
def sqlite_engine() -> ta.Generator[sa.engine.Engine, None, None]:
    engine: sa.engine.Engine
    with lang.disposing(
            sa.create_engine(
                'sqlite://',
                connect_args={'check_same_thread': False},
                poolclass=sa.pool.StaticPool,
            )
    ) as engine:
        yield engine
