import json
import shlex
import subprocess
import sys
import typing as ta

from ... import check
from ... import collections as col
from ... import dataclasses as dc
from ... import properties


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
