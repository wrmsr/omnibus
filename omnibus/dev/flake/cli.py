import configparser
import os.path

from ... import argparse as ap
from ... import logs


class Cli(ap.Cli):

    @ap.command()
    def run(self) -> None:
        if os.path.isfile('setup.cfg'):
            config = configparser.RawConfigParser()
            config.read('setup.cfg')
            print(config.items('flake8'))


def main():
    logs.configure_standard_logging()
    Cli()()


if __name__ == '__main__':
    main()
