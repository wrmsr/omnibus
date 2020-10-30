from cpython.buffer cimport PyBUF_ANY_CONTIGUOUS
from cpython.buffer cimport PyBUF_SIMPLE
from cpython.buffer cimport PyBuffer_Release
from cpython.buffer cimport PyObject_GetBuffer
from libc.stdint cimport int32_t


cdef class BufferView:
    cdef object o
    cdef Py_buffer buf

    def __cinit__(self, object o):
        self.o = o
        PyObject_GetBuffer(o, &self.buf, PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)

    def __dealloc__(self):
        PyBuffer_Release(&self.buf)


def add(int a, int b):
    return a + b


def add_int32_raw(size_t a, size_t b, size_t c, size_t l):
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pc = <int32_t *> c
    cdef size_t i = 0
    while i < l:
        pc[i] = pa[i] + pb[i]
        i += 1


def add_int32(a, b, c, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bc = BufferView(c)
    add_int32_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bc.buf.buf, l)
