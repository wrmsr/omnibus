import typing as ta

from .. import lang
from ..serde.formats import yaml


lang.warn_unstable()


def reorder_cfg_service_ports(cfg: dict) -> dict:
    return cfg


def main():
    with open('docker/docker-compose.yml') as r:
        buf = r.read()

    import pprint

    wcfg = yaml.load(buf, yaml.WrappedLoaders.Full)
    pprint.pprint(wcfg)

    cfg = yaml.full_load(buf)
    pprint.pprint(cfg)

    rocfg = reorder_cfg_service_ports(cfg)
    pprint.pprint(rocfg)

    import yaml as yaml_
    print(yaml_.dump(rocfg, default_flow_style=False))


if __name__ == '__main__':
    main()
