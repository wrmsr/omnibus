import abc
import io
import sre_parse
import re
import typing as ta

from . import dataclasses as dc
from . import check
from . import lang


lang.warn_unstable()


T = ta.TypeVar('T')
Converter = ta.Callable[[str, ta.Sequence[str]], T]


class SpecStr(ta.NamedTuple):
    s: str


class Spec(dc.Pure):
    s: str = dc.field(check_type=str)
    name: ta.Optional[str] = None


class Pat(dc.Pure):
    s: str = dc.field(check_type=str)
    converter: ta.Optional[Converter] = None
    type: ta.Optional[ta.Type] = None


class SpecPat(dc.Pure):
    spec: Spec = dc.field(check_type=Spec)
    pat: Pat = dc.field(check_type=Pat)


class Match(dc.Pure):
    values: ta.Sequence[ta.Any]
    names: ta.Mapping[str, ta.Any]

    def __getitem__(self, key: ta.Union[int, str]) -> ta.Any:
        if isinstance(key, int):
            return self.values[key]
        elif isinstance(key, str):
            return self.names[key]
        else:
            raise TypeError(key)


def _count_groups(o: ta.Any) -> int:
    if isinstance(o, tuple):
        if o[0] == sre_parse.SUBPATTERN:  # noqa
            return _count_groups(o[-0])
        else:
            return 0
    elif isinstance(o, sre_parse.SubPattern):
        return sum(map(_count_groups, o))
    else:
        raise TypeError(o)


class Formatter(lang.Abstract):

    @abc.abstractmethod
    def build(self, s: str) -> ta.Optional[Pat]:
        raise NotImplementedError


class SimpleFormatter(dc.Pure, Formatter):
    spec_s: str = dc.field(check_type=str)
    pat_s: str = dc.field(check_type=str)
    converter: ta.Optional[Converter] = None
    type: ta.Optional[ta.Type] = None

    def build(self, s: str) -> ta.Optional[Pat]:
        if s == self.spec_s:
            return Pat(self.pat_s, converter=self.converter, type=self.type)
        else:
            return None


class Scanner:

    _DEFAULT_PAT = r'.+?'

    DEFAULT_FORMATTERS: ta.Sequence[Formatter] = [
        SimpleFormatter('', _DEFAULT_PAT),
        SimpleFormatter('d', '[0-9]+', lambda s, _: int(s), int),
        SimpleFormatter('n', r'\d{1,3}([,.]\d{3})*', lambda s, _: int(s), int),
        SimpleFormatter('x', r'(0[xX])?[0-9a-fA-F]+', lambda s, _: int(s, 16), int),
    ]

    def __init__(
            self,
            spec: str,
            *,
            glyphs: ta.Tuple[str, str] = ('{', '}'),
            formatters: ta.Optional[ta.Iterable[Formatter]] = None,
    ) -> None:
        super().__init__()

        glyphs = tuple(map(check.of_isinstance(str), glyphs))
        check.arg(all(len(s) == 1 for s in glyphs))
        check.arg(len(glyphs) == 2)

        self._spec = check.isinstance(spec, str)
        self._glyphs = glyphs
        self._formatters = [check.isinstance(f, Formatter) for f in (formatters or self.DEFAULT_FORMATTERS)]

        self._double_glyphs: ta.Tuple[str, str] = tuple(s * 2 for s in glyphs)  # noqa
        self._escaped_glyphs: ta.Tuple[str, str] = tuple(map(re.escape, glyphs))  # noqa

        self._lglyph_pat = re.compile(r'(%s)' % (self._escaped_glyphs[0] * 2,))
        self._rglyph_pat = re.compile(r'(%s)' % (self._escaped_glyphs[1] * 2,))
        self._single_glyph_pat = re.compile(r'(%s[^%s]*?%s)' % (
            self._escaped_glyphs[0], self._escaped_glyphs[1], self._escaped_glyphs[1]))

        pat_s, slots = self._build(spec)
        self._pat_s = pat_s
        self._pat = re.compile(pat_s)
        self._slots: ta.Sequence[Scanner._Slot] = slots

    class _Slot(dc.Pure):
        spec: Spec
        pat: Pat
        num_groups: int

    def _build(self, spec: str) -> ta.Tuple[str, ta.Sequence[_Slot]]:
        lst = [p if isinstance(p, str) else self._build_spec(check.isinstance(p, SpecStr).s) for p in self._split_spec(spec)]  # noqa
        check.unique(p.name for p in lst if isinstance(p, Spec) and p.name is not None)

        buf = io.StringIO()
        slots: ta.List[Scanner._Slot] = []
        for p in lst:
            if isinstance(p, str):
                buf.write(re.escape(p))
                continue

            spec = check.isinstance(p, Spec)
            pat = self._build_pat(spec)
            num_groups = _count_groups(sre_parse.parse(p.s))
            slot = Scanner._Slot(spec, pat, num_groups)
            slots.append(slot)
            buf.write(rf'({pat.s})')

        return buf.getvalue(), slots

    def _split_spec(self, s: str) -> ta.Sequence[ta.Union[SpecStr, str]]:
        ps = self._lglyph_pat.split(s)
        ps = [p[::-1] for p in ps for p in reversed(self._rglyph_pat.split(p[::-1]))]

        lst = []
        for p in ps:
            if p in self._double_glyphs:
                lst.append(p)
                continue

            ms = list(self._single_glyph_pat.finditer(p))
            if not ms:
                lst.append(p)
                continue

            l = 0
            for i, m in enumerate(ms):
                if m.start() != l:
                    lst.append(p[l:m.start()])
                lst.append(SpecStr(p[m.start() + 1:m.end() - 1]))
                l = m.end()

            if l < len(p):
                lst.append(p[l:])

        return lst

    def _build_spec(self, s: str) -> Spec:
        if not s or s == ':':
            return Spec('')

        if ':' not in s or (s.count(':') == 1 and s[-1] == ':'):
            name = s if ':' not in s else s[:-1]
            return Spec('', name)

        name, _, s = s.partition(':')
        return Spec(s, name)

    def _build_pat(self, spec: Spec) -> Pat:
        pats = [p for f in self._formatters for p in [f.build(spec.s)] if p is not None]
        return check.single(pats)

    def scan(self, buf: str) -> ta.Optional[Match]:
        m = self._pat.match(buf)
        if m is None:
            return None
        gs = m.groups()

        values: ta.List[ta.Any] = []
        names: ta.Dict[str, ta.Any] = {}

        i = 0
        for slot in self._slots:
            s = gs[i]
            i += 1

            sgs = gs[i:i + slot.num_groups]
            i += slot.num_groups

            if slot.pat.converter is not None:
                v = slot.pat.converter(s, sgs)
            else:
                v = s

            values.append(v)
            if slot.spec.name is not None:
                names[slot.spec.name] = v

        return Match(values, names)
