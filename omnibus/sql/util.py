import contextlib
import io
import typing as ta

import sqlalchemy as sa
import sqlalchemy.exc  # noqa

from .. import check


def yield_sql_statements(body: str) -> ta.Iterator[str]:
    """Lame and shameful."""

    buf = io.StringIO()
    for line in body.split('\n'):
        stripped = line.strip()
        if stripped.startswith('--'):
            continue
        check.arg('/*' not in stripped)
        check.arg(stripped.rfind(';', 0, -1) < 0)
        if stripped.endswith(';'):
            buf.write(line.rpartition(';')[0])
            stmt = buf.getvalue().strip()
            if stmt:
                yield stmt
            buf = io.StringIO()
        else:
            buf.write(line)
            buf.write('\n')
    if buf.tell() > 0:
        stmt = buf.getvalue().strip()
        if stmt:
            yield stmt


@contextlib.contextmanager
def transaction_context(
        conn: sa.engine.Connection,
        *,
        passthrough: bool = False,
        nonest: bool = False,
) -> ta.Iterator[ta.Optional[sa.engine.Transaction]]:
    if passthrough:
        yield None
    elif nonest and conn.in_transaction():
        yield None
    else:
        transaction = conn.begin()
        state = None

        def hook(method_name, new_state):
            def inner(*args, **kwargs):
                nonlocal state
                state = new_state
                return old(*args, **kwargs)

            old = getattr(transaction, method_name)
            setattr(transaction, method_name, inner)

        hook('_do_commit', 'commit')
        hook('_do_rollback', 'rollback')

        try:
            yield transaction

            if not transaction._parent.is_active:  # type: ignore
                raise sa.exc.InvalidRequestError(f'This transaction is inactive: state={state}')

            transaction.commit()

        except Exception:
            if transaction._parent.is_active:  # type: ignore
                transaction.rollback()

            raise
