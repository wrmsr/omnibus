try:
    from billiard import *  # noqa
    from billiard import process  # noqa
    from billiard import queues  # noqa

except ImportError:
    from multiprocessing import *  # noqa
    from multiprocessing import process  # noqa
    from multiprocessing import queues  # noqa
