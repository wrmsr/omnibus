from cpython.buffer cimport PyBUF_ANY_CONTIGUOUS
from cpython.buffer cimport PyBUF_SIMPLE
from cpython.buffer cimport PyBuffer_Release
from cpython.buffer cimport PyObject_GetBuffer


cdef class BufferView:
    cdef object o
    cdef Py_buffer buf

    def __cinit__(self, object o):
        self.o = o
        PyObject_GetBuffer(o, &self.buf, PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)

    def __dealloc__(self):
        PyBuffer_Release(&self.buf)





from libc.stdint cimport int8_t
from libc.stdint cimport int16_t
from libc.stdint cimport int32_t
from libc.stdint cimport int64_t
from libc.stdint cimport uint8_t
from libc.stdint cimport uint16_t
from libc.stdint cimport uint32_t
from libc.stdint cimport uint64_t



cpdef add_int8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] + pb[i])
        i += 1


def add_int8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_int8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_int8_const_raw(size_t a, int8_t c, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] + c)
        i += 1


def add_int8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    add_int8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_int8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] - pb[i])
        i += 1


def sub_int8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_int8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_int8_const_raw(size_t a, int8_t c, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] - c)
        i += 1


def sub_int8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    sub_int8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_int8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] * pb[i])
        i += 1


def mul_int8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_int8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_int8_const_raw(size_t a, int8_t c, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] * c)
        i += 1


def mul_int8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    mul_int8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_int8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] / pb[i])
        i += 1


def div_int8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_int8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_int8_const_raw(size_t a, int8_t c, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] / c)
        i += 1


def div_int8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    div_int8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_int8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] % pb[i])
        i += 1


def mod_int8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_int8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_int8_const_raw(size_t a, int8_t c, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] % c)
        i += 1


def mod_int8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    mod_int8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef and_int8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] & pb[i])
        i += 1


def and_int8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    and_int8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef and_int8_const_raw(size_t a, int8_t c, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] & c)
        i += 1


def and_int8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    and_int8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef or_int8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] | pb[i])
        i += 1


def or_int8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    or_int8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef or_int8_const_raw(size_t a, int8_t c, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] | c)
        i += 1


def or_int8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    or_int8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef xor_int8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] ^ pb[i])
        i += 1


def xor_int8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    xor_int8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef xor_int8_const_raw(size_t a, int8_t c, size_t d, size_t l):
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] ^ c)
        i += 1


def xor_int8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    xor_int8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_int16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] + pb[i])
        i += 1


def add_int16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_int16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_int16_const_raw(size_t a, int16_t c, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] + c)
        i += 1


def add_int16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    add_int16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_int16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] - pb[i])
        i += 1


def sub_int16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_int16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_int16_const_raw(size_t a, int16_t c, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] - c)
        i += 1


def sub_int16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    sub_int16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_int16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] * pb[i])
        i += 1


def mul_int16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_int16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_int16_const_raw(size_t a, int16_t c, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] * c)
        i += 1


def mul_int16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    mul_int16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_int16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] / pb[i])
        i += 1


def div_int16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_int16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_int16_const_raw(size_t a, int16_t c, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] / c)
        i += 1


def div_int16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    div_int16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_int16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] % pb[i])
        i += 1


def mod_int16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_int16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_int16_const_raw(size_t a, int16_t c, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] % c)
        i += 1


def mod_int16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    mod_int16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef and_int16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] & pb[i])
        i += 1


def and_int16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    and_int16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef and_int16_const_raw(size_t a, int16_t c, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] & c)
        i += 1


def and_int16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    and_int16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef or_int16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] | pb[i])
        i += 1


def or_int16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    or_int16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef or_int16_const_raw(size_t a, int16_t c, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] | c)
        i += 1


def or_int16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    or_int16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef xor_int16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] ^ pb[i])
        i += 1


def xor_int16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    xor_int16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef xor_int16_const_raw(size_t a, int16_t c, size_t d, size_t l):
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] ^ c)
        i += 1


def xor_int16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    xor_int16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_int32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] + pb[i])
        i += 1


def add_int32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_int32_const_raw(size_t a, int32_t c, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] + c)
        i += 1


def add_int32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    add_int32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_int32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] - pb[i])
        i += 1


def sub_int32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_int32_const_raw(size_t a, int32_t c, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] - c)
        i += 1


def sub_int32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    sub_int32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_int32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] * pb[i])
        i += 1


def mul_int32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_int32_const_raw(size_t a, int32_t c, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] * c)
        i += 1


def mul_int32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    mul_int32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_int32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] / pb[i])
        i += 1


def div_int32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_int32_const_raw(size_t a, int32_t c, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] / c)
        i += 1


def div_int32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    div_int32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_int32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] % pb[i])
        i += 1


def mod_int32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_int32_const_raw(size_t a, int32_t c, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] % c)
        i += 1


def mod_int32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    mod_int32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef and_int32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] & pb[i])
        i += 1


def and_int32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    and_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef and_int32_const_raw(size_t a, int32_t c, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] & c)
        i += 1


def and_int32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    and_int32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef or_int32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] | pb[i])
        i += 1


def or_int32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    or_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef or_int32_const_raw(size_t a, int32_t c, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] | c)
        i += 1


def or_int32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    or_int32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef xor_int32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] ^ pb[i])
        i += 1


def xor_int32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    xor_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef xor_int32_const_raw(size_t a, int32_t c, size_t d, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] ^ c)
        i += 1


def xor_int32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    xor_int32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_int64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] + pb[i])
        i += 1


def add_int64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_int64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_int64_const_raw(size_t a, int64_t c, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] + c)
        i += 1


def add_int64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    add_int64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_int64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] - pb[i])
        i += 1


def sub_int64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_int64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_int64_const_raw(size_t a, int64_t c, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] - c)
        i += 1


def sub_int64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    sub_int64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_int64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] * pb[i])
        i += 1


def mul_int64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_int64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_int64_const_raw(size_t a, int64_t c, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] * c)
        i += 1


def mul_int64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    mul_int64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_int64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] / pb[i])
        i += 1


def div_int64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_int64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_int64_const_raw(size_t a, int64_t c, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] / c)
        i += 1


def div_int64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    div_int64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_int64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] % pb[i])
        i += 1


def mod_int64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_int64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_int64_const_raw(size_t a, int64_t c, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] % c)
        i += 1


def mod_int64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    mod_int64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef and_int64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] & pb[i])
        i += 1


def and_int64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    and_int64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef and_int64_const_raw(size_t a, int64_t c, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] & c)
        i += 1


def and_int64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    and_int64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef or_int64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] | pb[i])
        i += 1


def or_int64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    or_int64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef or_int64_const_raw(size_t a, int64_t c, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] | c)
        i += 1


def or_int64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    or_int64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef xor_int64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] ^ pb[i])
        i += 1


def xor_int64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    xor_int64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef xor_int64_const_raw(size_t a, int64_t c, size_t d, size_t l):
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] ^ c)
        i += 1


def xor_int64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    xor_int64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_uint8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] + pb[i])
        i += 1


def add_uint8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_uint8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_uint8_const_raw(size_t a, uint8_t c, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] + c)
        i += 1


def add_uint8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    add_uint8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_uint8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] - pb[i])
        i += 1


def sub_uint8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_uint8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_uint8_const_raw(size_t a, uint8_t c, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] - c)
        i += 1


def sub_uint8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    sub_uint8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_uint8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] * pb[i])
        i += 1


def mul_uint8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_uint8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_uint8_const_raw(size_t a, uint8_t c, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] * c)
        i += 1


def mul_uint8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    mul_uint8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_uint8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] / pb[i])
        i += 1


def div_uint8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_uint8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_uint8_const_raw(size_t a, uint8_t c, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] / c)
        i += 1


def div_uint8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    div_uint8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_uint8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] % pb[i])
        i += 1


def mod_uint8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_uint8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_uint8_const_raw(size_t a, uint8_t c, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] % c)
        i += 1


def mod_uint8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    mod_uint8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef and_uint8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] & pb[i])
        i += 1


def and_uint8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    and_uint8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef and_uint8_const_raw(size_t a, uint8_t c, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] & c)
        i += 1


def and_uint8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    and_uint8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef or_uint8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] | pb[i])
        i += 1


def or_uint8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    or_uint8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef or_uint8_const_raw(size_t a, uint8_t c, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] | c)
        i += 1


def or_uint8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    or_uint8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef xor_uint8_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] ^ pb[i])
        i += 1


def xor_uint8(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    xor_uint8_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef xor_uint8_const_raw(size_t a, uint8_t c, size_t d, size_t l):
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] ^ c)
        i += 1


def xor_uint8_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    xor_uint8_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_uint16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] + pb[i])
        i += 1


def add_uint16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_uint16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_uint16_const_raw(size_t a, uint16_t c, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] + c)
        i += 1


def add_uint16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    add_uint16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_uint16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] - pb[i])
        i += 1


def sub_uint16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_uint16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_uint16_const_raw(size_t a, uint16_t c, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] - c)
        i += 1


def sub_uint16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    sub_uint16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_uint16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] * pb[i])
        i += 1


def mul_uint16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_uint16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_uint16_const_raw(size_t a, uint16_t c, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] * c)
        i += 1


def mul_uint16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    mul_uint16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_uint16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] / pb[i])
        i += 1


def div_uint16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_uint16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_uint16_const_raw(size_t a, uint16_t c, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] / c)
        i += 1


def div_uint16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    div_uint16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_uint16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] % pb[i])
        i += 1


def mod_uint16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_uint16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_uint16_const_raw(size_t a, uint16_t c, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] % c)
        i += 1


def mod_uint16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    mod_uint16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef and_uint16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] & pb[i])
        i += 1


def and_uint16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    and_uint16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef and_uint16_const_raw(size_t a, uint16_t c, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] & c)
        i += 1


def and_uint16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    and_uint16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef or_uint16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] | pb[i])
        i += 1


def or_uint16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    or_uint16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef or_uint16_const_raw(size_t a, uint16_t c, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] | c)
        i += 1


def or_uint16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    or_uint16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef xor_uint16_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] ^ pb[i])
        i += 1


def xor_uint16(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    xor_uint16_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef xor_uint16_const_raw(size_t a, uint16_t c, size_t d, size_t l):
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] ^ c)
        i += 1


def xor_uint16_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    xor_uint16_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_uint32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] + pb[i])
        i += 1


def add_uint32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_uint32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_uint32_const_raw(size_t a, uint32_t c, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] + c)
        i += 1


def add_uint32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    add_uint32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_uint32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] - pb[i])
        i += 1


def sub_uint32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_uint32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_uint32_const_raw(size_t a, uint32_t c, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] - c)
        i += 1


def sub_uint32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    sub_uint32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_uint32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] * pb[i])
        i += 1


def mul_uint32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_uint32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_uint32_const_raw(size_t a, uint32_t c, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] * c)
        i += 1


def mul_uint32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    mul_uint32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_uint32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] / pb[i])
        i += 1


def div_uint32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_uint32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_uint32_const_raw(size_t a, uint32_t c, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] / c)
        i += 1


def div_uint32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    div_uint32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_uint32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] % pb[i])
        i += 1


def mod_uint32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_uint32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_uint32_const_raw(size_t a, uint32_t c, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] % c)
        i += 1


def mod_uint32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    mod_uint32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef and_uint32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] & pb[i])
        i += 1


def and_uint32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    and_uint32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef and_uint32_const_raw(size_t a, uint32_t c, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] & c)
        i += 1


def and_uint32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    and_uint32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef or_uint32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] | pb[i])
        i += 1


def or_uint32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    or_uint32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef or_uint32_const_raw(size_t a, uint32_t c, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] | c)
        i += 1


def or_uint32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    or_uint32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef xor_uint32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] ^ pb[i])
        i += 1


def xor_uint32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    xor_uint32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef xor_uint32_const_raw(size_t a, uint32_t c, size_t d, size_t l):
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] ^ c)
        i += 1


def xor_uint32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    xor_uint32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_uint64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] + pb[i])
        i += 1


def add_uint64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_uint64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_uint64_const_raw(size_t a, uint64_t c, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] + c)
        i += 1


def add_uint64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    add_uint64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_uint64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] - pb[i])
        i += 1


def sub_uint64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_uint64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_uint64_const_raw(size_t a, uint64_t c, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] - c)
        i += 1


def sub_uint64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    sub_uint64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_uint64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] * pb[i])
        i += 1


def mul_uint64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_uint64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_uint64_const_raw(size_t a, uint64_t c, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] * c)
        i += 1


def mul_uint64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    mul_uint64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_uint64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] / pb[i])
        i += 1


def div_uint64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_uint64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_uint64_const_raw(size_t a, uint64_t c, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] / c)
        i += 1


def div_uint64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    div_uint64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_uint64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] % pb[i])
        i += 1


def mod_uint64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_uint64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_uint64_const_raw(size_t a, uint64_t c, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] % c)
        i += 1


def mod_uint64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    mod_uint64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef and_uint64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] & pb[i])
        i += 1


def and_uint64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    and_uint64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef and_uint64_const_raw(size_t a, uint64_t c, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] & c)
        i += 1


def and_uint64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    and_uint64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef or_uint64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] | pb[i])
        i += 1


def or_uint64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    or_uint64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef or_uint64_const_raw(size_t a, uint64_t c, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] | c)
        i += 1


def or_uint64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    or_uint64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef xor_uint64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] ^ pb[i])
        i += 1


def xor_uint64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    xor_uint64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef xor_uint64_const_raw(size_t a, uint64_t c, size_t d, size_t l):
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] ^ c)
        i += 1


def xor_uint64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    xor_uint64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_float32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] + pb[i])
        i += 1


def add_float32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_float32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_float32_const_raw(size_t a, float c, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] + c)
        i += 1


def add_float32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef float cc = <float> c
    cdef BufferView bd = BufferView(d)
    add_float32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_float32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] - pb[i])
        i += 1


def sub_float32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_float32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_float32_const_raw(size_t a, float c, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] - c)
        i += 1


def sub_float32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef float cc = <float> c
    cdef BufferView bd = BufferView(d)
    sub_float32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_float32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] * pb[i])
        i += 1


def mul_float32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_float32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_float32_const_raw(size_t a, float c, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] * c)
        i += 1


def mul_float32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef float cc = <float> c
    cdef BufferView bd = BufferView(d)
    mul_float32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_float32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] / pb[i])
        i += 1


def div_float32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_float32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_float32_const_raw(size_t a, float c, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] / c)
        i += 1


def div_float32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef float cc = <float> c
    cdef BufferView bd = BufferView(d)
    div_float32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_float32_raw(size_t a, size_t b, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] % pb[i])
        i += 1


def mod_float32(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_float32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_float32_const_raw(size_t a, float c, size_t d, size_t l):
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] % c)
        i += 1


def mod_float32_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef float cc = <float> c
    cdef BufferView bd = BufferView(d)
    mod_float32_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef add_float64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] + pb[i])
        i += 1


def add_float64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    add_float64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef add_float64_const_raw(size_t a, double c, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] + c)
        i += 1


def add_float64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef double cc = <double> c
    cdef BufferView bd = BufferView(d)
    add_float64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef sub_float64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] - pb[i])
        i += 1


def sub_float64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    sub_float64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef sub_float64_const_raw(size_t a, double c, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] - c)
        i += 1


def sub_float64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef double cc = <double> c
    cdef BufferView bd = BufferView(d)
    sub_float64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mul_float64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] * pb[i])
        i += 1


def mul_float64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mul_float64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mul_float64_const_raw(size_t a, double c, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] * c)
        i += 1


def mul_float64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef double cc = <double> c
    cdef BufferView bd = BufferView(d)
    mul_float64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef div_float64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] / pb[i])
        i += 1


def div_float64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    div_float64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef div_float64_const_raw(size_t a, double c, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] / c)
        i += 1


def div_float64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef double cc = <double> c
    cdef BufferView bd = BufferView(d)
    div_float64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)


cpdef mod_float64_raw(size_t a, size_t b, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] % pb[i])
        i += 1


def mod_float64(a, b, d, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    mod_float64_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bd.buf.buf, l)


cpdef mod_float64_const_raw(size_t a, double c, size_t d, size_t l):
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] % c)
        i += 1


def mod_float64_const(a, c, d, l):
    cdef BufferView ba = BufferView(a)
    cdef double cc = <double> c
    cdef BufferView bd = BufferView(d)
    mod_float64_const_raw(<size_t> ba.buf.buf, cc, <size_t> bd.buf.buf, l)

