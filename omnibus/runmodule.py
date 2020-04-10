import runpy
import sys


def main():
    # Run the module specified as the next command line argument
    if len(sys.argv) < 2:
        print('No module specified for execution', file=sys.stderr)
    else:
        del sys.argv[0]  # Make the requested module sys.argv[0]
        runpy._run_module_as_main(sys.argv[0])  # noqa


if __name__ == '__main__':
    sys.exit(main())
