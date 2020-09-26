def pytest_configure(config):
    config.addinivalue_line('filterwarnings', 'ignore:omnibus module is marked as unstable::omnibus.*:')
