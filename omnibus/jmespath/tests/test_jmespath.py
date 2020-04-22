from .. import parsing as parsing_


def test_jmespath():
    node = parsing_.parse("locations[?state == 'WA'].name | sort(@) | {WashingtonCities: join(', ', @)}")
    print(node)
