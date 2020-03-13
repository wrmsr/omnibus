import typing as ta


def dumb_parse_lines(lines: ta.Iterable[str]) -> ta.Iterable[ta.Tuple[str, str]]:
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, _, v = line.partition('=')
        else:
            k, v = line, ''
        k = k.strip()
        v = v.strip().strip("'").strip('"')
        yield k, v
