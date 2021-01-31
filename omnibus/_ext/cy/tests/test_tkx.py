import tkinter as tk

import pytest  # noqa

from .. import tkx


@pytest.mark.skip()
def test_tk():
    root = tk.Tk()

    w = 256
    h = 256

    panel = tk.Label(root)
    img = tk.PhotoImage(width=w, height=h)
    pixels = bytearray()
    for y in range(h):
        for x in range(w):
            pixels.extend([0, y, x])
    pixels = bytes(pixels)
    tkx.photo_put(img, w, h, pixels)
    panel.configure(image=img)
    panel.pack(side='bottom', fill='both', expand='yes')
    root.mainloop()


if __name__ == '__main__':
    test_tk()
