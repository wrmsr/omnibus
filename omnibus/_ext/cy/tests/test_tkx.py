import tkinter as tk

import pytest

from .. import tkx


@pytest.mark.skip()
def test_tk():
    root = tk.Tk()

    w = 200
    h = 100

    panel = tk.Label(root)
    img = tk.PhotoImage(width=w, height=h)
    pixels = b'\0\xFF\0\0' * (w * h)
    tkx.photo_put(img, w, h, pixels)
    panel.configure(image=img)
    panel.pack(side='bottom', fill='both', expand='yes')
    root.mainloop()


if __name__ == '__main__':
    test_tk()
