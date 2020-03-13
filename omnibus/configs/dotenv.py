"""
https://github.com/kojiromike/parameter_expansion/blob/master/pe.py
"""
import typing as ta

from .. import check


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


class Parser:

    def __init__(self, buf: str) -> None:
        super().__init__()

        self._buf = check.isinstance(buf, str)
        self._pos = 0

    def read_pattern(self, pat: ta.Pattern) -> ta.Match:
        match = check.not_none(pat.match(self._buf, self._pos))
        check.state(match.end() >= self._pos)
        self._pos = match.end()
        return match


def parse(buf: str) -> ta.Iterable[ta.Tuple[str, ta.Optional[str]]]:
    raise NotImplementedError
