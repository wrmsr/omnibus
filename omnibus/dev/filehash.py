import os.path
import subprocess

from .. import argparse as ap
from .. import dataclasses as dc
from .. import json


class Entry(dc.Pure):
    name: str
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
        for fn in sorted(os.listdir(dp)):
            fp = os.path.abspath(os.path.join(dp, fn))
            if not os.path.isfile(fp):
                continue
            bmd5 = subprocess.check_output(['md5', '-q', fp])
            md5 = bmd5.decode('utf-8').strip()
            entry = Entry(
                name=fn,
                size=os.path.getsize(fp),
                mtime=os.path.getmtime(fp),
                md5=md5,
            )
            print(entry)


def main():
    cli = Cli()
    cli()


if __name__ == '__main__':
    main()
