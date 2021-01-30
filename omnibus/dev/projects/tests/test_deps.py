"""
https://www.python.org/dev/peps/pep-0508/#names
https://github.com/pypa/packaging
"""
import json
import os.path
import re
import shlex
import subprocess
import sys
import typing as ta

import pytest  # noqa

from .... import check
from .... import collections as col
from .... import dataclasses as dc
from .... import dispatch
from .... import lang
from .... import properties
from ...._vendor import antlr4  # noqa
from ...deps import parsing as dp


T = ta.TypeVar('T')


class Operator(dc.Pure):
    name: str
    glyph: str
    desc: str


class Operators(lang.ValueEnum[Operator]):
    GT = Operator('gt', '>', 'Any version greater than the specified version.')
    LT = Operator('lt', '<', 'Any version less than the specified version.')
    LTE = Operator('lte', '<=', 'Any version less than or equal to the specified version.')
    GTE = Operator('gte', '>=', 'Any version greater than or equal to the specified version.')
    EQ = Operator('eq', '==', 'Exactly the specified version.')
    NE = Operator('ne', '!=', 'Any version not equal to the specified version.')
    EX = Operator('ex', '~=', 'Any compatible release. Compatible releases are releases that are within the same major or minor version, assuming the package author is using semantic versioning.')  # noqa
    ALL = Operator('all', '*', 'Can be used at the end of a version number to represent all.')


class Comment(dc.Frozen):
    s: str = dc.field(check_type=str, check=lambda s: s.startswith('#'))

    @property
    def hot(self) -> ta.Optional[str]:
        return self.s[2:].strip() if self.s.startswith('#@') else None

    @properties.cached
    def level(self) -> int:
        for i, c in enumerate(self.s):
            if c != '#':
                return i
        return len(self.s)

    @classmethod
    def of(cls, obj: ta.Union['Comment', str]) -> 'Comment':
        if isinstance(obj, Comment):
            return obj
        elif isinstance(obj, str):
            return cls(obj.strip())
        else:
            raise TypeError(obj)


class Comments(dc.Pure, ta.Sequence[Comment]):
    seq: ta.Sequence[Comment] = dc.field((), coerce=col.seq_of(Comment.of))

    def __iter__(self) -> ta.Iterator[Comment]:
        return iter(self.seq)

    def __getitem__(self, k: ta.Any) -> ta.Sequence[Comment]:
        return self.seq[k]

    def __len__(self) -> int:
        return len(self.seq)

    @classmethod
    def of(cls, obj: ta.Union['Comments', ta.Iterable[ta.Union[Comment, str]]]) -> 'Comments':
        if isinstance(obj, Comments):
            return obj
        elif isinstance(obj, str):
            raise TypeError(obj)
        elif isinstance(obj, ta.Iterable):
            return cls(list(obj))
        else:
            raise TypeError(obj)

    @classmethod
    def split(cls, s: str) -> 'Comments':
        ss = re.split(r'(#[#@\s$]#*)', s.strip())
        check.empty(ss[0])
        del ss[0]
        check.state(len(ss) % 2 == 0)
        return cls([
            Comment(p)
            for l, r in zip(ss[::2], ss[1::2])
            for l, r in [(l.strip(), r.strip())]
            for p in [l + (r if l.endswith('@') else (' ' + r))]
            for p in [p.strip()]
            if p
        ])


def render_comments(cmts: ta.Iterable[Comment]) -> str:
    return '  '.join(c.s.strip() for c in cmts)


class Line(dc.Enum, reorder=True):
    linum: ta.Optional[int] = dc.field(None, kwonly=True)
    raw: ta.Optional[str] = dc.field(None, kwonly=True)


class DepLine(Line):
    dep: dp.NameDep
    comments: ta.Optional[Comments] = dc.field(None, kwonly=True, coerce=Comments.of)

    @properties.cached
    def hot_comments(self) -> ta.Sequence[str]:
        return [h for c in check.not_none(self.comments) for h in [c.hot] if h is not None]


class IncludeLine(Line):
    name: str
    comments: Comments = dc.field(Comments(), coerce=Comments.of)


class CommentLine(Line):
    comments: Comments = dc.field(coerce=Comments.of)


class BlankLine(Line):
    pass


class LineRenderer(dispatch.Class):
    __call__ = dispatch.property()

    def __call__(self, l: Line) -> str:  # noqa
        raise TypeError(l)

    def __call__(self, l: DepLine) -> str:  # noqa
        s = dp.render(l.dep)
        if l.comments:
            s += '  ' + render_comments(l.comments)
        return s

    def __call__(self, l: IncludeLine) -> str:  # noqa
        s = f'-r {l.name}'
        if l.comments:
            s += render_comments(l.comments)
        return s

    def __call__(self, l: CommentLine) -> str:  # noqa
        return render_comments(l.comments)

    def __call__(self, l: BlankLine) -> str:  # noqa
        return ''


def render_line(l: Line) -> str:
    return LineRenderer()(l)


@dc.dataclass(frozen=True)
class DepFile:
    path: str = dc.field(coerce=check.non_empty_str)
    lines: ta.Sequence[Line] = dc.field(coerce=col.seq_of(check.of_isinstance(Line)))


@dc.dataclass(frozen=True)
class DepEnv:
    files: ta.Sequence[DepFile] = dc.field(coerce=col.seq_of(check.of_isinstance(DepFile)))

    @properties.cached
    @property
    def files_by_path(self) -> ta.Mapping[str, DepFile]:
        return col.unique_dict((f.path, f) for f in self.files)

    def get_lines(self, cls: ta.Type[T] = object) -> ta.Sequence[T]:
        return [l for f in self.files for l in f.lines if isinstance(l, cls)]

    @properties.cached
    @property
    def dep_lines(self) -> ta.Sequence[DepLine]:
        return self.get_lines(DepLine)

    @properties.cached
    @property
    def deps(self) -> ta.Sequence[dp.NameDep]:
        return [l.dep for l in self.dep_lines]


_INCLUDE_PAT = re.compile(r'-r\s*(?P<name>[^#]+)\s*(?P<comment>#.*)?')
_COMMENT_PAT = re.compile(r'(?P<comment>#.*)')


def build_dep_comments(dep: dp.NameDep) -> Comments:
    r = dep.meta.get(antlr4.ParserRuleContext)
    if r is None:
        return Comments()

    ps = [
        s
        for t in r.parser.getInputStream().tokens
        if t.channel == 1
        for s in [t.text.strip()]
        if s.startswith('#')
        and s
    ]
    if not ps:
        return Comments()

    return Comments.split('  '.join(ps))


def parse_line(raw: str, *, linum: ta.Optional[int] = None) -> Line:
    kw = dict(raw=raw)
    if linum is not None:
        kw.update(linum=linum)

    raw = raw.strip()
    if not raw:
        return BlankLine(**kw)

    m = _INCLUDE_PAT.fullmatch(raw)
    if m is not None:
        cmt = m.groupdict().get('comment')
        return IncludeLine(m.groupdict()['name'], [cmt] if cmt is not None else [], **kw)

    m = _COMMENT_PAT.fullmatch(raw)
    if m is not None:
        return CommentLine(Comments.split(m.groupdict()['comment']), **kw)

    dep = dp.parse(raw)
    cmts = build_dep_comments(dep)
    return DepLine(dep, comments=cmts, **kw)


def read_dep_file(file_name: str) -> DepFile:
    fp = os.path.abspath(file_name)
    with open(fp, 'r') as f:
        lines = f.readlines()

    dls = []
    for linum, raw in enumerate(lines):
        dl = parse_line(raw, linum=linum)
        dls.append(dl)

    return DepFile(fp, dls)


def read_dep_env(file_name: str) -> DepEnv:
    dirp, fn = os.path.split(os.path.abspath(file_name))
    files = {}
    todo = [os.path.join(dirp, fn)]
    while todo:
        fp = os.path.abspath(todo.pop())
        if fp in files:
            raise KeyError(fp)

        df = read_dep_file(fp)

        for dl in df.lines:
            if isinstance(dl, IncludeLine):
                nfp = os.path.abspath(os.path.join(dirp, dl.name))
                if nfp not in files:
                    todo.append(nfp)

        files[fp] = df

    return DepEnv(files.values())


class PipDep(dc.Pure):
    name: str
    version: str
    latest_version: str
    latest_filetype: str


class PipDeps(dc.Frozen, ta.Sequence[PipDep]):
    deps: ta.Sequence[PipDep] = dc.field(coerce=col.seq_of(check.of_isinstance(PipDep)))

    # @ta.overload
    # def __getitem__(self, s: slice) -> ta.Sequence[PipDep]: ...

    def __getitem__(self, i: int) -> PipDep:
        return self.deps[i]

    def __len__(self) -> int:
        return len(self.deps)

    @properties.cached
    @property
    def by_name(self) -> ta.Mapping[str, PipDep]:
        return col.unique_dict((d.name, d) for d in self.deps)


def get_pip_deps(*, interp: ta.Optional[str] = None) -> PipDeps:
    if interp is None:
        interp = sys.executable

    cmd = [interp, '-mpip', 'list', '-o', '--format=json']

    # Fucking piece of shit pydevd:
    #   https://github.com/fabioz/PyDev.Debugger/blob/179bdddc941a3f4d9400e96bcea79daac5d6144b/_pydev_bundle/pydev_monkey.py#L151
    cmd_str = ' '.join(map(shlex.quote, cmd))
    output = subprocess.check_output(cmd_str, shell=True)

    dcts = json.loads(output.decode('utf-8'))
    return PipDeps([PipDep(**dct) for dct in dcts])


@pytest.mark.skip
def test_deps():
    dirp = os.getcwd()
    fn = 'requirements-exp.txt'

    dirp = os.path.expanduser(dirp)
    fp = os.path.abspath(os.path.join(dirp, fn))

    de = read_dep_env(fp)

    explicit_dep_names = {d.name for d in de.deps}
    pinned_dep_names = {d.name for d in de.deps if any(v.op == '==' for v in d.vers)}

    pip_deps = get_pip_deps(interp=os.path.join(os.path.expanduser(dirp), '.venv/bin/python'))

    file_rewrites = {}
    for df in de.files:
        new_lines = []
        for line in df.lines:
            if isinstance(line, DepLine) and 'auto' in line.hot_comments and line.dep.name in pip_deps.by_name:
                pip_dep = pip_deps.by_name[line.dep.name]
                if len(line.dep.vers) == 1 and line.dep.vers[0] != pip_dep.latest_version:
                    line = dc.replace(line, dep=dc.replace(line.dep, vers=[dp.Version('==', pip_dep.latest_version)]))

            new_lines.append(render_line(line))

        file_rewrites[df.path] = '\n'.join(new_lines)

    disp_labels = ['Package', 'Version', 'Latest', 'Type']
    disp_atts = ['name', 'version', 'latest_version', 'latest_filetype']

    seen = set()
    ps = [
        max([len(l)] + [len(getattr(e, k)) for e in pip_deps if e.name not in seen])
        for l, k in zip(disp_labels, disp_atts)
    ]
    print(' '.join(l.ljust(p) for l, p in zip(disp_labels, ps)))

    for pred in [
        lambda n: n in pinned_dep_names,
        lambda n: n not in pinned_dep_names and n in explicit_dep_names,
        lambda n: n not in pinned_dep_names and n not in explicit_dep_names,
    ]:
        print(' '.join('-' * p for p in ps))
        for e in pip_deps:
            if e.name not in seen and pred(e.name.lower()):
                print(' '.join(getattr(e, k).ljust(p) for k, p in zip(disp_atts, ps)))
