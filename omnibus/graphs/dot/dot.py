"""
TODO:
 - import colorsys

https://github.com/chadbrewbaker/ReverseSnowflakeJoins/blob/master/dir.g lolwut
 - https://github.com/chadbrewbaker/ReverseSnowflakeJoins/blob/5a1186843b47db0c94d976ca115efa6012b572ba/gui.py#L37
 - * https://linux.die.net/man/1/gvpr *
 - https://github.com/rodw/gvpr-lib
"""
import abc
import html
import subprocess
import typing as ta

from ... import lang
from ... import os as oos


def escape(s: str) -> str:
    return html.escape(s).replace('@', '&#64;')


class Color(ta.NamedTuple):
    r: int
    g: int
    b: int


def gen_rainbow(steps: int) -> ta.List[Color]:
    colors = []
    for r in range(steps):
        colors.append(Color(r * 255 // steps, 255, 0))
    for g in range(steps, 0, -1):
        colors.append(Color(255, g * 255 // steps, 0))
    for b in range(steps):
        colors.append(Color(255, 0, b * 255 // steps))
    for r in range(steps, 0, -1):
        colors.append(Color(r * 255 // steps, 0, 255))
    for g in range(steps):
        colors.append(Color(0, g * 255 // steps, 255))
    for b in range(steps, 0, -1):
        colors.append(Color(0, 255, b * 255 // steps))
    colors.append(Color(0, 255, 0))
    return colors


class Renderable(lang.Abstract):

    @abc.abstractmethod
    def render(self, out) -> None:
        raise NotImplementedError


class Column(Renderable):
    pass


class Row(Renderable):
    pass


class Section(Renderable):
    pass


class Table(Renderable):
    pass


def open_dot(gv: str, *, timeout: float = 1.) -> None:
    stdout, _ = subprocess.Popen(
        ['dot', '-Tpdf'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    ).communicate(
        input=gv.encode('utf-8'),
        timeout=timeout,
    )

    with oos.tmp_file() as pdf:
        pdf.file.write(stdout)
        pdf.file.flush()

        _, _ = subprocess.Popen(
            ['open', pdf.name],
        ).communicate(
            timeout=timeout,
        )
