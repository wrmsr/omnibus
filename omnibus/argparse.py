import argparse
import typing as ta

from . import lang


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
