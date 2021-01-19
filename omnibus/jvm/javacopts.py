"""
https://docs.oracle.com/javase/7/docs/technotes/tools/windows/javac.html
"""
import abc
import typing as ta

from .. import check
from .. import lang


class Opt(lang.Abstract):

    @abc.abstractproperty
    def args(self) -> ta.Sequence[str]:
        raise NotImplementedError


class LiteralOpt(Opt):

    def __init__(self, *args: str) -> None:
        super().__init__()

        self._args = args

    @property
    def args(self) -> ta.Sequence[str]:
        return self._args


class VerboseOpt(Opt):
    args = ['-verbose']


class DebugOpts(lang.ValueEnum):
    ALL = '-g'
    NONE = '-g:none'
    LINES = '-g:lines'
    VARS = '-g:vars'
    SOURCE = '-g:source'


class LintOpts(lang.ValueEnum):
    RECOMMENDED = '-Xlint'
    ALL = '-Xlint:all'


class VersionOpt(Opt, lang.Abstract):

    DEFAULT_VERSION = 8

    def __init__(self, version: int = DEFAULT_VERSION) -> None:
        super().__init__()

        self._version = version

    @property
    def version(self) -> int:
        return self._version

    @abc.abstractproperty
    def prefix(self) -> str:
        raise NotImplementedError

    @property
    def args(self) -> ta.Sequence[str]:
        return [self.prefix, f'1.{self._version}']


class SourceVersionOpt(VersionOpt):
    prefix = '-source'


class TargetVersionOpt(VersionOpt):
    prefix = '-target'


class PathOpt(Opt, lang.Abstract):

    def __init__(self, path: str) -> None:
        super().__init__()

        self._path = check.not_empty(path)

    @property
    def path(self) -> str:
        return self._path

    @abc.abstractproperty
    def prefix(self) -> str:
        raise NotImplementedError

    @property
    def args(self) -> ta.Sequence[str]:
        return [self.prefix, self.path]


class ClasspathOpt(PathOpt):
    prefix = '-cp'


class HeaderOpt(PathOpt):
    prefix = '-h'


class OutputOpt(PathOpt):
    prefix = '-d'
