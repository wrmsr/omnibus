"""
TODO:
 - ignore state file
 - % done
"""
import concurrent.futures as cf
import contextlib
import gzip
import logging
import os.path
import subprocess
import threading
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


EntryMap = ta.MutableMapping[str, 'Entry']


class Entry(dc.Pure):
    name: str
    htime: float
    size: int
    mtime: float
    md5: str


class State(dc.Pure):
    entries_by_name: EntryMap

    def to_json(self) -> ta.Any:
        return {
            e.name: {
                k: v
                for k, v in dc.asdict(e).items()
                if k != 'name'
            }
            for e in sorted(self.entries_by_name.values(), key=lambda e: e.name)
        }

    @classmethod
    def from_json(cls, obj: ta.Mapping[str, ta.Mapping[str, ta.Any]]) -> 'State':
        return cls(
            entries_by_name={
                n: Entry(name=n, **d)
                for n, d in obj.items()
            }
        )


class Builder:

    class Config(dc.Pure):
        dir_path: ta.Optional[str] = None
        file_name: str = '.filehash'
        parallelism: ta.Optional[int] = None
        recursive: bool = False
        write_interval: ta.Optional[ta.Union[int, float]] = None

    def __init__(self, config: Config = Config()) -> None:
        super().__init__()

        self._config = check.isinstance(config, Builder.Config)

        self._state: State = State({})
        self._version = 0

    @property
    def config(self) -> Config:
        return self._config

    @property
    def state(self) -> State:
        return self._state

    @properties.cached
    def dir_path(self) -> str:
        dir_path = os.path.abspath(
            os.path.expanduser(self._config.dir_path) if self._config.dir_path is not None else os.getcwd())
        check.arg(os.path.isdir(dir_path))
        return dir_path

    @properties.cached
    def state_file_path(self) -> str:
        return os.path.join(self.dir_path, self._config.file_name)

    def _scan_files(self) -> ta.AbstractSet[str]:
        if self._config.recursive:
            fns = (os.path.join(dp, fn) for dp, dn, dfns in os.walk(self.dir_path) for fn in dfns)
        else:
            fns = os.listdir(self.dir_path)
        return set(fns)

    def build(self) -> None:
        with contextlib.ExitStack() as es:
            if self._config.write_interval is not None:
                es.enter_context(self._Writer(self))

            if self._config.parallelism is not None and self._config.parallelism > 0:
                exe = es.enter_context(cf.ThreadPoolExecutor(self._config.parallelism))
            else:
                exe = asyncs.ImmediateExecutor()

            fns = self._scan_files() | set(self._state.entries_by_name)
            futs = [exe.submit(self._build, fn) for fn in sorted(fns)]
            asyncs.await_futures(futs, raise_exceptions=True, timeout_s=60 * 60)

        if self._config.write_interval is not None:
            self.write()

    @logs.error_logging(log)
    def _build(self, file_name: str) -> None:
        log.info(f'Building {file_name}')
        file_path = os.path.abspath(os.path.join(self.dir_path, file_name))
        if not os.path.isfile(file_path):
            if file_name in self._state.entries_by_name:
                del self._state.entries_by_name[file_name]
                self._version += 1
            return

        check.state(file_path.startswith(self.dir_path))
        rel_file_path = file_path[len(self.dir_path):].lstrip(os.sep)

        htime = time.time()

        size = os.path.getsize(file_path)
        mtime = os.path.getmtime(file_path)

        entry = self._state.entries_by_name.get(rel_file_path)
        if entry is not None and entry.size == size and int(entry.mtime) == int(mtime):
            entry = dc.replace(entry, htime=htime)

        else:
            bmd5 = subprocess.check_output(['md5', '-q', file_path])
            md5 = bmd5.decode('utf-8').strip()
            entry = Entry(
                name=rel_file_path,
                htime=htime,
                size=size,
                mtime=mtime,
                md5=md5,
            )

        self._state.entries_by_name[entry.name] = entry
        self._version += 1

    def write(self) -> None:
        fp = os.path.join(self.dir_path, self._config.file_name)
        sz = sum(e.size for e in self._state.entries_by_name.values())
        content = self._state.to_json()
        buf = json.dumps(content, indent=True)
        buf = gzip.compress(buf.encode('utf-8'))
        with open(fp, 'wb') as f:
            f.write(buf)
        log.info(f'Wrote {fp} with {len(self._state.entries_by_name)} items, {sz:,} bytes, {len(buf):,} filesize')

    def read(self) -> ta.Optional[State]:
        fp = os.path.join(self.dir_path, self._config.file_name)
        if not os.path.isfile(fp):
            return None
        with open(fp, 'rb') as f:
            buf = f.read()
        try:
            buf = gzip.decompress(buf)
        except gzip.BadGzipFile:
            pass
        content = json.loads(buf.decode('utf-8'))
        return State.from_json(content)

    def load(self) -> None:
        state = self.read()
        if state is None:
            state = State({})
        self._state = state
        self._version += 1

    class _Writer:

        def __init__(self, builder: 'Builder') -> None:
            super().__init__()
            self._builder = builder
            self._thread: ta.Optional[threading.Thread] = None
            self._event = threading.Event()

        def __enter__(self) -> 'Builder._Writer':
            check.none(self._thread)
            self._thread = threading.Thread(target=self._proc, daemon=True)
            self._thread.start()
            return self

        @logs.error_logging(log)
        def _proc(self) -> None:
            log.info(f'Writer thread entering')
            version = -1
            while True:
                if self._event.wait(self._builder._config.write_interval):
                    break
                cur_version = self._builder._version
                if cur_version != version:
                    self._builder.write()
                    version = cur_version
            log.info(f'Writer thread exiting')

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self._thread is not None:
                self._event.set()
                self._thread.join()
            return None


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
            write_interval=60,
        ))

        builder.load()
        builder.build()

        entry_lists_by_hash: ta.Dict[str, ta.List[Entry]] = {}
        for e in builder.state.entries_by_name.values():
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
