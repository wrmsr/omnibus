import json
import os.path

from .. import parsing as parsing_


def test_jmespath():
    node = parsing_.parse("locations[?state == 'WA'].name | sort(@) | {WashingtonCities: join(', ', @)}")
    print(node)


def test_cases():
    path = os.path.join(os.path.dirname(__file__), 'json')
    for name in os.listdir(path):
        if not name.endswith('.json') or name == 'schema.json':
            continue
        with open(os.path.join(path, name), 'r') as f:
            buf = f.read()
        suites = json.loads(buf)

        for suite in suites:
            for case in suite['cases']:
                try:
                    node = parsing_.parse(case['expression'])
                except Exception as e:  # noqa
                    if case.get('error') == 'syntax':
                        continue
                    print(name)
                    print(case['expression'])
                    print(e)
                    print()
                else:
                    # print(node)
                    pass
