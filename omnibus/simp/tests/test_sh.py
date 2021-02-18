"""
https://github.com/docker-library/busybox/blob/844e23eae6a28fd1faf9b25f8ed977ae4b168a0f/stable/uclibc/Dockerfile
https://git.busybox.net/busybox/tree/shell/ash.c
"""
import ast
import inspect

from ..pyasts import translate


def barf():
    a = 'hi'
    b = 'why'
    c = a + b
    print(c)


def test_sh():
    a = translate(ast.parse(inspect.getsource(barf)))
    print(a)
