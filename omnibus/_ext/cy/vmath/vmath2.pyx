cimport cython

from libc.string cimport memset
from libcpp cimport bool

from cpython.buffer cimport PyBUF_ANY_CONTIGUOUS
from cpython.buffer cimport PyBUF_SIMPLE
from cpython.buffer cimport PyBuffer_Release
from cpython.buffer cimport PyObject_GetBuffer

from ._vmath2 cimport *

DEF MAX_ARGS = 16

cpdef op(size_t fn, args):
    cdef pfn_op_t pfn = <pfn_op_t> fn
    cdef OpArg op_args[MAX_ARGS]
    cdef bool is_buf[MAX_ARGS]
    cdef Py_buffer bufs[MAX_ARGS]
    cdef int i = 0

    memset(op_args, 0, sizeof(op_args))
    memset(is_buf, 0, sizeof(bool) * MAX_ARGS)

    exc = None
    for t, v in args:
        if i >= MAX_ARGS:
            exc = ValueError('Too many args')
            break

        if t == 'sz':
            op_args[i].sz = <size_t> v

        elif t.startswith('p'):
            is_buf[i] = 1
            PyObject_GetBuffer(v, &bufs[i], PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)
            op_args[i].p = bufs[i].buf

        elif t == 'i8':
            op_args[i].i8 = <int8_t> v
        elif t == 'i16':
            op_args[i].i16 = <int16_t> v
        elif t == 'i32':
            op_args[i].i32 = <int32_t> v
        elif t == 'i64':
            op_args[i].i64 = <int64_t> v

        elif t == 'u8':
            op_args[i].u8 = <uint8_t> v
        elif t == 'u16':
            op_args[i].u16 = <uint16_t> v
        elif t == 'u32':
            op_args[i].u32 = <uint32_t> v
        elif t == 'u64':
            op_args[i].u64 = <uint64_t> v

        elif t == 'f32':
            op_args[i].f32 = <float> v
        elif t == 'f64':
            op_args[i].f64 = <double> v

        else:
            exc = ValueError(f'Unhandled arg type: {t}')
            break

        i += 1

    if exc is None:
        pfn(op_args)

    i = 0
    while i < MAX_ARGS:
        if is_buf[i]:
            PyBuffer_Release(&bufs[i])
        i += 1

    if exc is not None:
        raise exc
