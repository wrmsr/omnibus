from .. import argparse as ap


class Cli(ap.Cli):

    path: str = ap.arg()

    @ap.command()
    def gen(self) -> None:
        print('gen')


def main():
    cli = Cli()
    cli()


if __name__ == '__main__':
    main()
