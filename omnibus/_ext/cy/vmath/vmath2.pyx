cimport cython

from libc.string cimport memset
from libcpp cimport bool

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

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef void _op_add_sz_pi8_pi8_pi8(void **args) nogil:
    cdef size_t a0 = <size_t> args[0]
    cdef int8_t *a1 = <int8_t *> args[1]
    cdef int8_t *a2 = <int8_t *> args[2]
    cdef int8_t *a3 = <int8_t *> args[3]
    cdef size_t i = 0
    while i < a0:
        a1[i] = <int8_t> (a2[i] + a3[i])
        i += 1

_pfn_op_add_sz_pf32_pf32_pf32 = <size_t> _op_add_sz_pf32_pf32_pf32

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef void _op_add_sz_pf32_pf32_pf32(void **args) nogil:
    cdef size_t a0 = <size_t> args[0]
    cdef float *a1 = <float *> args[1]
    cdef float *a2 = <float *> args[2]
    cdef float *a3 = <float *> args[3]
    cdef size_t i = 0
    while i < a0:
        a1[i] = <float> (a2[i] + a3[i])
        i += 1

_pfn_op_add_sz_pi8_pi8_pi8 = <size_t> _op_add_sz_pi8_pi8_pi8

ctypedef void (*pfn_op_t) (void **args) nogil

DEF MAX_ARGS = 16

cpdef op(size_t fn, args):
    cdef pfn_op_t pfn = <pfn_op_t> fn
    cdef void *aa[MAX_ARGS]
    cdef bool isbuf[MAX_ARGS]
    cdef Py_buffer bufs[MAX_ARGS]
    cdef int i = 0
    memset(isbuf, 0, sizeof(bool) * MAX_ARGS)

    exc = None
    for t, v in args:
        if i >= MAX_ARGS:
            exc = ValueError('Too many args')
            break

        if t == 'sz':
            (<size_t*> &aa[i])[0] = <size_t> v

        elif t == 'i8':
            (<int8_t*> &aa[i])[0] = <int8_t> v

        elif t == 'f32':
            (<float*> &aa[i])[0] = <float> v

        elif t in (
                'pi8',
                'pf32',
        ):
            isbuf[i] = 1
            PyObject_GetBuffer(v, &bufs[i], PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)
            aa[i] = bufs[i].buf

        else:
            exc = ValueError(f'Unhandled arg type: {t}')
            break

        i += 1

    if exc is None:
        pfn(aa)

    i = 0
    while i < MAX_ARGS:
        if isbuf[i]:
            PyBuffer_Release(&bufs[i])
        i += 1

    if exc is not None:
        raise exc
