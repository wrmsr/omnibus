import pytest

from .. import nginx as ng


def test_config():
    cfg = ng.ConfigItems.of([
        'abc;',
        'def;',
        ('ghi', [
            'a;',
            'b;',
            ('c', [
                'd;'
            ]),
        ]),
    ])
    print(cfg.render().getvalue())


@pytest.mark.xfail()
def test_nginx_process():
    with ng.NginxProcess() as proc:
        print(proc._config.connect_timeout)
        print(proc.nginx_version)
        print(proc.nginx_cfg_args)
