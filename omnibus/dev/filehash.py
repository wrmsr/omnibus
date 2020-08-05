import os.path
import subprocess
import time

from .. import argparse as ap
from .. import check
from .. import dataclasses as dc
from .. import json


class Entry(dc.Pure):
    name: str
    htime: float
    size: int
    mtime: float
    md5: str


class Builder:

    def __init__(self) -> None:
        super().__init__()

    def build(self) -> None:
        pass


class Cli(ap.Cli):

    @ap.command(
        ap.arg('-r', '--recursive', dest='recursive'),
    )
    def gen(self) -> None:
        dp = os.path.abspath(os.getcwd())
        ebn = {}
        for fn in sorted(os.listdir(dp)):
            fp = os.path.abspath(os.path.join(dp, fn))
            if not os.path.isfile(fp):
                continue
            htime = time.time()
            bmd5 = subprocess.check_output(['md5', '-q', fp])
            md5 = bmd5.decode('utf-8').strip()
            entry = Entry(
                name=fn,
                htime=htime,
                size=os.path.getsize(fp),
                mtime=os.path.getmtime(fp),
                md5=md5,
            )
            check.not_in(entry.name, ebn)
            ebn[entry.name] = entry

        dct = {
            e.name: {
                k: v
                for k, v in dc.asdict(e).items()
                if k != 'name'
            }
            for e in sorted(ebn.values(), key=lambda e: e.name)
        }
        print(json.dumps(dct, indent=True))


def main():
    cli = Cli()
    cli()


if __name__ == '__main__':
    main()
