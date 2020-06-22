from .. import javaopts


def test_jvmopts():
    assert javaopts.DEBUG() == '-Xdebug'
    assert javaopts.REMOTE_DEBUG(420, False) == '-Xrunjdwp:transport=dt_socket,address=420,server=y,suspend=n'
    assert javaopts.ALWAYS_PRE_TOUCH(True) == '-XX:+AlwaysPreTouch'
    assert javaopts.HEADLESS(True) == '-Djava.awt.headless=true'
    assert javaopts.MAX_HEAP_SIZE(2, javaopts.DataSize.GB) == '-Xmx2g'
