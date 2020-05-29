import os.path
import textwrap

import Cython.Compiler.Main

from .. import cython as cython_
from ... import os as oos


def compile_cpp(pyx: str) -> str:
    with oos.tmp_dir() as bp:
        pyxp = os.path.join(bp, 'test.pyx')
        cp = os.path.join(bp, 'test.cpp')

        with open(pyxp, 'w') as f:
            f.write(pyx)

        opts = Cython.Compiler.Main.CompilationOptions(
            language_level=3,
            cplus=True,
        )
        ret = Cython.Compiler.Main.compile_single(pyxp, opts)

        assert ret.num_errors == 0
        assert ret.c_file == cp
        assert ret.c_file_generated == 1

        with open(cp, 'r') as f:
            c = f.read()

        return c


def test_no_virtual():
    pyx = textwrap.dedent("""
    cpdef cppclass TextThing:

        int _val

        __init__(int _val):
            this._val = _val

        int get():
            return this._val
    """)

    c = compile_cpp(pyx)
    # print(c)
    assert c

    with cython_.patch_no_virtual_context():
        c = compile_cpp(pyx)
        # print(c)
        assert c
