from .. import pydevd


def main():
    pydevd.maybe_reexec(module=__package__ + '._daemon', silence=True)

    import pyspark.daemon
    pyspark.daemon.manager()


if __name__ == '__main__':
    main()
