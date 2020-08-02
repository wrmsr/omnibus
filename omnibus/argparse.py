import argparse
import dataclasses as dc
import sys
import typing as ta

from . import c3
from . import check
from . import lang
from . import properties


lang.warn_unstable()


T = ta.TypeVar('T')


ONE_OR_MORE = argparse.ONE_OR_MORE
OPTIONAL = argparse.OPTIONAL
PARSER = argparse.PARSER
REMAINDER = argparse.REMAINDER
SUPPRESS = argparse.SUPPRESS
ZERO_OR_MORE = argparse.ZERO_OR_MORE

Action = argparse.Action
ArgumentDefaultsHelpFormatter = argparse.ArgumentDefaultsHelpFormatter
ArgumentError = argparse.ArgumentError
ArgumentParser = argparse.ArgumentParser
FileType = argparse.FileType
HelpFormatter = argparse.HelpFormatter
MetavarTypeHelpFormatter = argparse.MetavarTypeHelpFormatter
Namespace = argparse.Namespace
RawDescriptionHelpFormatter = argparse.RawDescriptionHelpFormatter
RawTextHelpFormatter = argparse.RawTextHelpFormatter
SubParsersAction = argparse._SubParsersAction  # noqa


@dc.dataclass(frozen=True)
class Arg:
    args: ta.Sequence[ta.Any]
    kwargs: ta.Mapping[str, ta.Any]


def arg(*args, **kwargs) -> Arg:
    return Arg(args, kwargs)


@dc.dataclass(frozen=True)
class Command:
    fn: ta.Callable[[], None]
    args: ta.Sequence[Arg] = ()
    name: ta.Optional[str] = None
    parent: ta.Optional['Command'] = None


def command(
        *args: Arg,
        name: ta.Optional[str] = None,
        parent: ta.Optional[Command] = None,
):
    for arg in args:
        check.isinstance(arg, Arg)
    check.isinstance(name, (str, None))
    check.isinstance(parent, (Command, None))

    def inner(fn):
        return Command(
            fn,
            args,
            name=name,
            parent=parent,
        )

    return inner


class _CliMeta(type):

    def __new__(mcls, name: str, bases: ta.Sequence[type], namespace: ta.Mapping[str, ta.Any]) -> type:
        cmds = {}
        mro = c3.merge([list(b.__mro__) for b in bases])
        for bcls in reversed(mro):
            for k, v in bcls.__dict__.items():
                if isinstance(v, Command):
                    cmds[k] = v
                elif k in cmds:
                    del [k]

        cls = super().__new__(mcls, name, tuple(bases), dict(namespace))
        return cls


class Cli(metaclass=_CliMeta):

    def __init__(self, args: ta.Optional[ta.Sequence[str]] = None) -> None:
        super().__init__()

        self._args = args if args is not None else sys.argv

    _parser: ta.ClassVar[ArgumentParser]

    @properties.class_
    @classmethod
    def parser(cls) -> ArgumentParser:
        return cls._parser

    def __call__(self) -> None:
        raise NotImplementedError
