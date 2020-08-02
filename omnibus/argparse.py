import argparse
import dataclasses as dc
import functools
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


CommandFn = ta.Callable[[], None]


@dc.dataclass()
class Command:
    name: str
    fn: CommandFn
    args: ta.Sequence[Arg] = ()
    parent: ta.Optional['Command'] = None

    def __post_init__(self) -> None:
        check.isinstance(self.name, str)
        check.not_in('-', self.name)
        check.not_empty(self.name)

        check.callable(self.fn)
        check.arg(all(isinstance(a, Arg) for a in self.args))
        check.isinstance(self.parent, (Command, None))

        functools.update_wrapper(self, self.fn)


def command(
        *args: Arg,
        name: ta.Optional[str] = None,
        parent: ta.Optional[Command] = None,
) -> ta.Callable[[CommandFn], Command]:
    for arg in args:
        check.isinstance(arg, Arg)
    check.isinstance(name, (str, None))
    check.isinstance(parent, (Command, None))

    def inner(fn):
        return Command(
            (name if name is not None else fn.__name__).replace('-', '_'),
            fn,
            args,
            parent=parent,
        )

    return inner


class _CliMeta(type):

    def __new__(mcls, name: str, bases: ta.Sequence[type], namespace: ta.Mapping[str, ta.Any]) -> type:
        if not bases:
            return super().__new__(mcls, name, tuple(bases), dict(namespace))

        bases = list(bases)
        namespace = dict(namespace)

        cmds = {}
        mro = c3.merge([list(b.__mro__) for b in bases])
        for bns in [bcls.__dict__ for bcls in reversed(mro)] + [namespace]:
            for k, v in bns.items():
                if isinstance(v, Command):
                    cmds[k] = v
                elif k in cmds:
                    del [k]

        if 'parser' in namespace:
            parser = check.isinstance(namespace.pop('parser'), ArgumentParser)
        else:
            parser = ArgumentParser()
        namespace['_parser'] = parser

        subparsers = parser.add_subparsers()
        for cmd in cmds.values():
            cparser = subparsers.add_parser(cmd.name)
            for arg in (cmd.args or []):
                cparser.add_argument(*arg.args, **arg.kwargs)
            cparser.set_defaults(_cmd=cmd)

        cls = super().__new__(mcls, name, tuple(bases), namespace)
        return cls


class Cli(metaclass=_CliMeta):

    def __init__(self, argv: ta.Optional[ta.Sequence[str]] = None) -> None:
        super().__init__()

        self._argv = argv if argv is not None else sys.argv[1:]
        self._args = self.parser.parse_args(self._argv)

    _parser: ta.ClassVar[ArgumentParser]

    @properties.class_
    @classmethod
    def parser(cls) -> ArgumentParser:
        return cls._parser

    @property
    def argv(self) -> ta.Sequence[str]:
        return self._argv

    @property
    def args(self) -> Namespace:
        return self._args

    def _run_cmd(self, cmd: Command) -> None:
        cmd.fn.__get__(self, type(self))()

    def __call__(self) -> None:
        cmd = getattr(self.args, '_cmd', None)
        if cmd is None:
            self.parser.print_help()
            return
        self._run_cmd(cmd)
