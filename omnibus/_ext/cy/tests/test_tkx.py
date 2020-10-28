import tkinter as tk

import pytest

from .. import tkx


@pytest.mark.skip()
def test_tk():
    root = tk.Tk()
    tkx.init(root.interpaddr())
