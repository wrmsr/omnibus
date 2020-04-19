from .. import persistent as p_


def test_persistent():
    a = p_.SimplePersistentSequence(range(3))  # noqa
    b = p_.PyrsistentSequence(range(3))  # noqa
