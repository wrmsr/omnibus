import typing as ta


def camelize(name: str) -> str:
    return ''.join(map(str.capitalize, name.split('_')))


def decamelize(name: str) -> str:
    uppers: ta.List[ta.Optional[int]] = [i for i, c in enumerate(name) if c.isupper()]
    return '_'.join([name[l:r].lower() for l, r in zip([None] + uppers, uppers + [None])]).strip('_')


def prefix_lines(s: str, p: str) -> str:
    return '\n'.join([p + l for l in s.split('\n')])


def indent_lines(s: str, num: int) -> str:
    return prefix_lines(s, ' ' * num)


def is_dunder(name: str) -> bool:
    return (
            name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4
    )


def is_sunder(name: str) -> bool:
    return (
            name[0] == name[-1] == '_' and
            name[1:2] != '_' and
            name[-2:-1] != '_' and
            len(name) > 2
    )
