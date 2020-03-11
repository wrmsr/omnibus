import io
import typing as ta

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
