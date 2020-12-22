import concurrent.futures as cf
import logging
import os.path
import subprocess
import time
import typing as ta

from ... import argparse as ap
from ... import asyncs
from ... import check
from ... import dataclasses as dc
from ... import json
from ... import logs
from ... import properties


log = logging.getLogger(__name__)


class Entry(dc.Pure):
    name: str
    htime: float
    size: int
    mtime: float
    md5: str


class Builder:

    class Config(dc.Pure):
        dir_path: ta.Optional[str] = None
        file_name: str = '.filehash'
        parallelism: ta.Optional[int] = None
        recursive: bool = False

    def __init__(self, config: Config = Config()) -> None:
        super().__init__()

        self._config = check.isinstance(config, Builder.Config)

        self._entries_by_name: ta.MutableMapping[str, Entry] = {}

    @property
    def config(self) -> Config:
        return self._config

    @property
    def entries_by_name(self) -> ta.Mapping[str, Entry]:
        return self._entries_by_name

    @properties.cached
    def dir_path(self) -> str:
        dir_path = os.path.abspath(
            os.path.expanduser(self._config.dir_path) if self._config.dir_path is not None else os.getcwd())
        check.arg(os.path.isdir(dir_path))
        return dir_path

    def build(self) -> None:
        if self._config.parallelism is not None and self._config.parallelism > 0:
            exe = cf.ThreadPoolExecutor(self._config.parallelism)
        else:
            exe = asyncs.ImmediateExecutor()
        with exe:
            if self._config.recursive:
                fns = (os.path.join(dp, fn) for dp, dn, dfns in os.walk(self.dir_path) for fn in dfns)
            else:
                fns = os.listdir(self.dir_path)
            futs = [exe.submit(self._build, fn) for fn in sorted(fns)]
            asyncs.await_futures(futs, raise_exceptions=True)

    def _build(self, file_name: str) -> None:
        log.info(f'Building {file_name}')
        file_path = os.path.abspath(os.path.join(self.dir_path, file_name))
        if not os.path.isfile(file_path):
            if file_name in self._entries_by_name:
                del self._entries_by_name[file_name]
            return
        check.state(file_path.startswith(self.dir_path))
        rel_file_path = file_path[len(self.dir_path):].lstrip(os.sep)

        htime = time.time()
        bmd5 = subprocess.check_output(['md5', '-q', file_path])
        md5 = bmd5.decode('utf-8').strip()
        entry = Entry(
            name=rel_file_path,
            htime=htime,
            size=os.path.getsize(file_path),
            mtime=os.path.getmtime(file_path),
            md5=md5,
        )

        self._entries_by_name[entry.name] = entry

    def build_content(self) -> ta.Any:
        return {
            e.name: {
                k: v
                for k, v in dc.asdict(e).items()
                if k != 'name'
            }
            for e in sorted(self._entries_by_name.values(), key=lambda e: e.name)
        }

    def write(self) -> None:
        content = self.build_content()
        with open(os.path.join(self.dir_path, self._config.file_name), 'w') as f:
            f.write(json.dumps(content, indent=True))

    def print(self) -> None:
        print(json.dumps(self.build_content(), indent=True))


class Cli(ap.Cli):

    dir_path: str = ap.arg('-d', '--dir-path')
    parallelism: int = ap.arg('-p', '--parallelism')
    recursive: bool = ap.arg('-r', '--recursive')

    @ap.command()
    def gen(self) -> None:
        builder = Builder(Builder.Config(
            dir_path=self.dir_path,
            parallelism=self.parallelism,
            recursive=self.recursive,
        ))

        builder.build()

        # builder.print()

        entry_lists_by_hash: ta.Dict[str, ta.List[Entry]] = {}
        for e in builder.entries_by_name.values():
            entry_lists_by_hash.setdefault(e.md5, []).append(e)
        for l in entry_lists_by_hash.values():
            if len(l) > 1:
                print(json.dumps([dc.asdict(e) for e in l], indent=True))


def main():
    logs.configure_standard_logging(logging.INFO)
    cli = Cli()
    cli()


if __name__ == '__main__':
    main()
