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


<%
    int_szs = [8, 16, 32, 64]
    int_typs = [f'{p}int{sz}' for p in ['', 'u'] for sz in int_szs]

    op_tups = [
        ('add', '+'),
        ('sub', '-'),
        ('mul', '*'),
        ('div', '/'),
        ('mod', '%'),

        ('and', '&'),
        ('or', '|'),
        ('xor', '^'),
    ]
%>


% for typ in int_typs:
from libc.stdint cimport ${typ}_t
% endfor


% for typ in int_typs:
% for op_nam, op_s in op_tups:

cpdef ${op_nam}_${typ}_raw(size_t a, size_t b, size_t c, size_t l):
    cdef ${typ}_t *pa = <${typ}_t *> a
    cdef ${typ}_t *pb = <${typ}_t *> b
    cdef ${typ}_t *pc = <${typ}_t *> c
    cdef size_t i = 0
    while i < l:
        pc[i] = <${typ}_t> (pa[i] ${op_s} pb[i])
        i += 1


def ${op_nam}_${typ}(a, b, c, l):
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bc = BufferView(c)
    ${op_nam}_${typ}_raw(<size_t> ba.buf.buf, <size_t> bb.buf.buf, <size_t> bc.buf.buf, l)

% endfor
% endfor