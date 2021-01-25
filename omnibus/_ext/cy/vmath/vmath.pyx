"""
TODO:
 - non-cpdef inners, single gateway that takes fn ptr, globall dct of fn ptrs by name/spec/whatever
"""
cimport cython

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







ctypedef void (*pfn_op_int8_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_int8_const_t) (void *a, int8_t c, void *d, size_t l) nogil


cpdef op_int8_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_int8_t pfn = <pfn_op_int8_t> <size_t> fn
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    pfn(pa, pb, pd, l)


cpdef op_int8(fn, a, b, d, l):
    cdef pfn_op_int8_t pfn = <pfn_op_int8_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_int8_const_raw(size_t fn, size_t a, int8_t c, size_t d, size_t l):
    cdef pfn_op_int8_const_t pfn = <pfn_op_int8_const_t> <size_t> fn
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    pfn(pa, c, pd, l)


cpdef op_int8_const(fn, a, c, d, l):
    cdef pfn_op_int8_const_t pfn = <pfn_op_int8_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef int8_t cc = <int8_t> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_int8(void *a, void *b, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] + pb[i])
        i += 1

_pfn_add_int8 = <size_t> _add_int8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_int8_const(void *a, int8_t c, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] + c)
        i += 1


_pfn_add_int8_const = <size_t> _add_int8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_int8(void *a, void *b, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] - pb[i])
        i += 1

_pfn_sub_int8 = <size_t> _sub_int8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_int8_const(void *a, int8_t c, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] - c)
        i += 1


_pfn_sub_int8_const = <size_t> _sub_int8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_int8(void *a, void *b, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] * pb[i])
        i += 1

_pfn_mul_int8 = <size_t> _mul_int8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_int8_const(void *a, int8_t c, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] * c)
        i += 1


_pfn_mul_int8_const = <size_t> _mul_int8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_int8(void *a, void *b, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] / pb[i])
        i += 1

_pfn_div_int8 = <size_t> _div_int8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_int8_const(void *a, int8_t c, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] / c)
        i += 1


_pfn_div_int8_const = <size_t> _div_int8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_int8(void *a, void *b, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] % pb[i])
        i += 1

_pfn_mod_int8 = <size_t> _mod_int8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_int8_const(void *a, int8_t c, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] % c)
        i += 1


_pfn_mod_int8_const = <size_t> _mod_int8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_int8(void *a, void *b, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] & pb[i])
        i += 1

_pfn_and_int8 = <size_t> _and_int8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_int8_const(void *a, int8_t c, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] & c)
        i += 1


_pfn_and_int8_const = <size_t> _and_int8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_int8(void *a, void *b, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] | pb[i])
        i += 1

_pfn_or_int8 = <size_t> _or_int8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_int8_const(void *a, int8_t c, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] | c)
        i += 1


_pfn_or_int8_const = <size_t> _or_int8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_int8(void *a, void *b, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pb = <int8_t *> b
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] ^ pb[i])
        i += 1

_pfn_xor_int8 = <size_t> _xor_int8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_int8_const(void *a, int8_t c, void *d, size_t l) nogil:
    cdef int8_t *pa = <int8_t *> a
    cdef int8_t *pd = <int8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int8_t> (pa[i] ^ c)
        i += 1


_pfn_xor_int8_const = <size_t> _xor_int8_const




ctypedef void (*pfn_op_int16_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_int16_const_t) (void *a, int16_t c, void *d, size_t l) nogil


cpdef op_int16_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_int16_t pfn = <pfn_op_int16_t> <size_t> fn
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    pfn(pa, pb, pd, l)


cpdef op_int16(fn, a, b, d, l):
    cdef pfn_op_int16_t pfn = <pfn_op_int16_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_int16_const_raw(size_t fn, size_t a, int16_t c, size_t d, size_t l):
    cdef pfn_op_int16_const_t pfn = <pfn_op_int16_const_t> <size_t> fn
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    pfn(pa, c, pd, l)


cpdef op_int16_const(fn, a, c, d, l):
    cdef pfn_op_int16_const_t pfn = <pfn_op_int16_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef int16_t cc = <int16_t> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_int16(void *a, void *b, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] + pb[i])
        i += 1

_pfn_add_int16 = <size_t> _add_int16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_int16_const(void *a, int16_t c, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] + c)
        i += 1


_pfn_add_int16_const = <size_t> _add_int16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_int16(void *a, void *b, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] - pb[i])
        i += 1

_pfn_sub_int16 = <size_t> _sub_int16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_int16_const(void *a, int16_t c, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] - c)
        i += 1


_pfn_sub_int16_const = <size_t> _sub_int16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_int16(void *a, void *b, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] * pb[i])
        i += 1

_pfn_mul_int16 = <size_t> _mul_int16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_int16_const(void *a, int16_t c, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] * c)
        i += 1


_pfn_mul_int16_const = <size_t> _mul_int16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_int16(void *a, void *b, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] / pb[i])
        i += 1

_pfn_div_int16 = <size_t> _div_int16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_int16_const(void *a, int16_t c, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] / c)
        i += 1


_pfn_div_int16_const = <size_t> _div_int16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_int16(void *a, void *b, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] % pb[i])
        i += 1

_pfn_mod_int16 = <size_t> _mod_int16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_int16_const(void *a, int16_t c, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] % c)
        i += 1


_pfn_mod_int16_const = <size_t> _mod_int16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_int16(void *a, void *b, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] & pb[i])
        i += 1

_pfn_and_int16 = <size_t> _and_int16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_int16_const(void *a, int16_t c, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] & c)
        i += 1


_pfn_and_int16_const = <size_t> _and_int16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_int16(void *a, void *b, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] | pb[i])
        i += 1

_pfn_or_int16 = <size_t> _or_int16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_int16_const(void *a, int16_t c, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] | c)
        i += 1


_pfn_or_int16_const = <size_t> _or_int16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_int16(void *a, void *b, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pb = <int16_t *> b
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] ^ pb[i])
        i += 1

_pfn_xor_int16 = <size_t> _xor_int16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_int16_const(void *a, int16_t c, void *d, size_t l) nogil:
    cdef int16_t *pa = <int16_t *> a
    cdef int16_t *pd = <int16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int16_t> (pa[i] ^ c)
        i += 1


_pfn_xor_int16_const = <size_t> _xor_int16_const




ctypedef void (*pfn_op_int32_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_int32_const_t) (void *a, int32_t c, void *d, size_t l) nogil


cpdef op_int32_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_int32_t pfn = <pfn_op_int32_t> <size_t> fn
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    pfn(pa, pb, pd, l)


cpdef op_int32(fn, a, b, d, l):
    cdef pfn_op_int32_t pfn = <pfn_op_int32_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_int32_const_raw(size_t fn, size_t a, int32_t c, size_t d, size_t l):
    cdef pfn_op_int32_const_t pfn = <pfn_op_int32_const_t> <size_t> fn
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    pfn(pa, c, pd, l)


cpdef op_int32_const(fn, a, c, d, l):
    cdef pfn_op_int32_const_t pfn = <pfn_op_int32_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef int32_t cc = <int32_t> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_int32(void *a, void *b, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] + pb[i])
        i += 1

_pfn_add_int32 = <size_t> _add_int32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_int32_const(void *a, int32_t c, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] + c)
        i += 1


_pfn_add_int32_const = <size_t> _add_int32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_int32(void *a, void *b, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] - pb[i])
        i += 1

_pfn_sub_int32 = <size_t> _sub_int32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_int32_const(void *a, int32_t c, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] - c)
        i += 1


_pfn_sub_int32_const = <size_t> _sub_int32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_int32(void *a, void *b, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] * pb[i])
        i += 1

_pfn_mul_int32 = <size_t> _mul_int32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_int32_const(void *a, int32_t c, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] * c)
        i += 1


_pfn_mul_int32_const = <size_t> _mul_int32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_int32(void *a, void *b, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] / pb[i])
        i += 1

_pfn_div_int32 = <size_t> _div_int32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_int32_const(void *a, int32_t c, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] / c)
        i += 1


_pfn_div_int32_const = <size_t> _div_int32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_int32(void *a, void *b, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] % pb[i])
        i += 1

_pfn_mod_int32 = <size_t> _mod_int32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_int32_const(void *a, int32_t c, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] % c)
        i += 1


_pfn_mod_int32_const = <size_t> _mod_int32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_int32(void *a, void *b, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] & pb[i])
        i += 1

_pfn_and_int32 = <size_t> _and_int32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_int32_const(void *a, int32_t c, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] & c)
        i += 1


_pfn_and_int32_const = <size_t> _and_int32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_int32(void *a, void *b, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] | pb[i])
        i += 1

_pfn_or_int32 = <size_t> _or_int32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_int32_const(void *a, int32_t c, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] | c)
        i += 1


_pfn_or_int32_const = <size_t> _or_int32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_int32(void *a, void *b, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pb = <int32_t *> b
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] ^ pb[i])
        i += 1

_pfn_xor_int32 = <size_t> _xor_int32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_int32_const(void *a, int32_t c, void *d, size_t l) nogil:
    cdef int32_t *pa = <int32_t *> a
    cdef int32_t *pd = <int32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int32_t> (pa[i] ^ c)
        i += 1


_pfn_xor_int32_const = <size_t> _xor_int32_const




ctypedef void (*pfn_op_int64_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_int64_const_t) (void *a, int64_t c, void *d, size_t l) nogil


cpdef op_int64_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_int64_t pfn = <pfn_op_int64_t> <size_t> fn
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    pfn(pa, pb, pd, l)


cpdef op_int64(fn, a, b, d, l):
    cdef pfn_op_int64_t pfn = <pfn_op_int64_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_int64_const_raw(size_t fn, size_t a, int64_t c, size_t d, size_t l):
    cdef pfn_op_int64_const_t pfn = <pfn_op_int64_const_t> <size_t> fn
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    pfn(pa, c, pd, l)


cpdef op_int64_const(fn, a, c, d, l):
    cdef pfn_op_int64_const_t pfn = <pfn_op_int64_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef int64_t cc = <int64_t> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_int64(void *a, void *b, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] + pb[i])
        i += 1

_pfn_add_int64 = <size_t> _add_int64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_int64_const(void *a, int64_t c, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] + c)
        i += 1


_pfn_add_int64_const = <size_t> _add_int64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_int64(void *a, void *b, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] - pb[i])
        i += 1

_pfn_sub_int64 = <size_t> _sub_int64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_int64_const(void *a, int64_t c, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] - c)
        i += 1


_pfn_sub_int64_const = <size_t> _sub_int64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_int64(void *a, void *b, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] * pb[i])
        i += 1

_pfn_mul_int64 = <size_t> _mul_int64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_int64_const(void *a, int64_t c, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] * c)
        i += 1


_pfn_mul_int64_const = <size_t> _mul_int64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_int64(void *a, void *b, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] / pb[i])
        i += 1

_pfn_div_int64 = <size_t> _div_int64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_int64_const(void *a, int64_t c, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] / c)
        i += 1


_pfn_div_int64_const = <size_t> _div_int64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_int64(void *a, void *b, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] % pb[i])
        i += 1

_pfn_mod_int64 = <size_t> _mod_int64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_int64_const(void *a, int64_t c, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] % c)
        i += 1


_pfn_mod_int64_const = <size_t> _mod_int64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_int64(void *a, void *b, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] & pb[i])
        i += 1

_pfn_and_int64 = <size_t> _and_int64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_int64_const(void *a, int64_t c, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] & c)
        i += 1


_pfn_and_int64_const = <size_t> _and_int64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_int64(void *a, void *b, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] | pb[i])
        i += 1

_pfn_or_int64 = <size_t> _or_int64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_int64_const(void *a, int64_t c, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] | c)
        i += 1


_pfn_or_int64_const = <size_t> _or_int64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_int64(void *a, void *b, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pb = <int64_t *> b
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] ^ pb[i])
        i += 1

_pfn_xor_int64 = <size_t> _xor_int64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_int64_const(void *a, int64_t c, void *d, size_t l) nogil:
    cdef int64_t *pa = <int64_t *> a
    cdef int64_t *pd = <int64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <int64_t> (pa[i] ^ c)
        i += 1


_pfn_xor_int64_const = <size_t> _xor_int64_const




ctypedef void (*pfn_op_uint8_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_uint8_const_t) (void *a, uint8_t c, void *d, size_t l) nogil


cpdef op_uint8_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_uint8_t pfn = <pfn_op_uint8_t> <size_t> fn
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    pfn(pa, pb, pd, l)


cpdef op_uint8(fn, a, b, d, l):
    cdef pfn_op_uint8_t pfn = <pfn_op_uint8_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_uint8_const_raw(size_t fn, size_t a, uint8_t c, size_t d, size_t l):
    cdef pfn_op_uint8_const_t pfn = <pfn_op_uint8_const_t> <size_t> fn
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    pfn(pa, c, pd, l)


cpdef op_uint8_const(fn, a, c, d, l):
    cdef pfn_op_uint8_const_t pfn = <pfn_op_uint8_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef uint8_t cc = <uint8_t> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_uint8(void *a, void *b, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] + pb[i])
        i += 1

_pfn_add_uint8 = <size_t> _add_uint8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_uint8_const(void *a, uint8_t c, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] + c)
        i += 1


_pfn_add_uint8_const = <size_t> _add_uint8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_uint8(void *a, void *b, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] - pb[i])
        i += 1

_pfn_sub_uint8 = <size_t> _sub_uint8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_uint8_const(void *a, uint8_t c, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] - c)
        i += 1


_pfn_sub_uint8_const = <size_t> _sub_uint8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_uint8(void *a, void *b, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] * pb[i])
        i += 1

_pfn_mul_uint8 = <size_t> _mul_uint8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_uint8_const(void *a, uint8_t c, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] * c)
        i += 1


_pfn_mul_uint8_const = <size_t> _mul_uint8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_uint8(void *a, void *b, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] / pb[i])
        i += 1

_pfn_div_uint8 = <size_t> _div_uint8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_uint8_const(void *a, uint8_t c, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] / c)
        i += 1


_pfn_div_uint8_const = <size_t> _div_uint8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_uint8(void *a, void *b, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] % pb[i])
        i += 1

_pfn_mod_uint8 = <size_t> _mod_uint8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_uint8_const(void *a, uint8_t c, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] % c)
        i += 1


_pfn_mod_uint8_const = <size_t> _mod_uint8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_uint8(void *a, void *b, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] & pb[i])
        i += 1

_pfn_and_uint8 = <size_t> _and_uint8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_uint8_const(void *a, uint8_t c, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] & c)
        i += 1


_pfn_and_uint8_const = <size_t> _and_uint8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_uint8(void *a, void *b, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] | pb[i])
        i += 1

_pfn_or_uint8 = <size_t> _or_uint8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_uint8_const(void *a, uint8_t c, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] | c)
        i += 1


_pfn_or_uint8_const = <size_t> _or_uint8_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_uint8(void *a, void *b, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pb = <uint8_t *> b
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] ^ pb[i])
        i += 1

_pfn_xor_uint8 = <size_t> _xor_uint8



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_uint8_const(void *a, uint8_t c, void *d, size_t l) nogil:
    cdef uint8_t *pa = <uint8_t *> a
    cdef uint8_t *pd = <uint8_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint8_t> (pa[i] ^ c)
        i += 1


_pfn_xor_uint8_const = <size_t> _xor_uint8_const




ctypedef void (*pfn_op_uint16_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_uint16_const_t) (void *a, uint16_t c, void *d, size_t l) nogil


cpdef op_uint16_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_uint16_t pfn = <pfn_op_uint16_t> <size_t> fn
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    pfn(pa, pb, pd, l)


cpdef op_uint16(fn, a, b, d, l):
    cdef pfn_op_uint16_t pfn = <pfn_op_uint16_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_uint16_const_raw(size_t fn, size_t a, uint16_t c, size_t d, size_t l):
    cdef pfn_op_uint16_const_t pfn = <pfn_op_uint16_const_t> <size_t> fn
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    pfn(pa, c, pd, l)


cpdef op_uint16_const(fn, a, c, d, l):
    cdef pfn_op_uint16_const_t pfn = <pfn_op_uint16_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef uint16_t cc = <uint16_t> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_uint16(void *a, void *b, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] + pb[i])
        i += 1

_pfn_add_uint16 = <size_t> _add_uint16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_uint16_const(void *a, uint16_t c, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] + c)
        i += 1


_pfn_add_uint16_const = <size_t> _add_uint16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_uint16(void *a, void *b, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] - pb[i])
        i += 1

_pfn_sub_uint16 = <size_t> _sub_uint16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_uint16_const(void *a, uint16_t c, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] - c)
        i += 1


_pfn_sub_uint16_const = <size_t> _sub_uint16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_uint16(void *a, void *b, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] * pb[i])
        i += 1

_pfn_mul_uint16 = <size_t> _mul_uint16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_uint16_const(void *a, uint16_t c, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] * c)
        i += 1


_pfn_mul_uint16_const = <size_t> _mul_uint16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_uint16(void *a, void *b, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] / pb[i])
        i += 1

_pfn_div_uint16 = <size_t> _div_uint16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_uint16_const(void *a, uint16_t c, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] / c)
        i += 1


_pfn_div_uint16_const = <size_t> _div_uint16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_uint16(void *a, void *b, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] % pb[i])
        i += 1

_pfn_mod_uint16 = <size_t> _mod_uint16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_uint16_const(void *a, uint16_t c, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] % c)
        i += 1


_pfn_mod_uint16_const = <size_t> _mod_uint16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_uint16(void *a, void *b, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] & pb[i])
        i += 1

_pfn_and_uint16 = <size_t> _and_uint16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_uint16_const(void *a, uint16_t c, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] & c)
        i += 1


_pfn_and_uint16_const = <size_t> _and_uint16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_uint16(void *a, void *b, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] | pb[i])
        i += 1

_pfn_or_uint16 = <size_t> _or_uint16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_uint16_const(void *a, uint16_t c, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] | c)
        i += 1


_pfn_or_uint16_const = <size_t> _or_uint16_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_uint16(void *a, void *b, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pb = <uint16_t *> b
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] ^ pb[i])
        i += 1

_pfn_xor_uint16 = <size_t> _xor_uint16



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_uint16_const(void *a, uint16_t c, void *d, size_t l) nogil:
    cdef uint16_t *pa = <uint16_t *> a
    cdef uint16_t *pd = <uint16_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint16_t> (pa[i] ^ c)
        i += 1


_pfn_xor_uint16_const = <size_t> _xor_uint16_const




ctypedef void (*pfn_op_uint32_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_uint32_const_t) (void *a, uint32_t c, void *d, size_t l) nogil


cpdef op_uint32_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_uint32_t pfn = <pfn_op_uint32_t> <size_t> fn
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    pfn(pa, pb, pd, l)


cpdef op_uint32(fn, a, b, d, l):
    cdef pfn_op_uint32_t pfn = <pfn_op_uint32_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_uint32_const_raw(size_t fn, size_t a, uint32_t c, size_t d, size_t l):
    cdef pfn_op_uint32_const_t pfn = <pfn_op_uint32_const_t> <size_t> fn
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    pfn(pa, c, pd, l)


cpdef op_uint32_const(fn, a, c, d, l):
    cdef pfn_op_uint32_const_t pfn = <pfn_op_uint32_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef uint32_t cc = <uint32_t> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_uint32(void *a, void *b, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] + pb[i])
        i += 1

_pfn_add_uint32 = <size_t> _add_uint32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_uint32_const(void *a, uint32_t c, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] + c)
        i += 1


_pfn_add_uint32_const = <size_t> _add_uint32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_uint32(void *a, void *b, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] - pb[i])
        i += 1

_pfn_sub_uint32 = <size_t> _sub_uint32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_uint32_const(void *a, uint32_t c, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] - c)
        i += 1


_pfn_sub_uint32_const = <size_t> _sub_uint32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_uint32(void *a, void *b, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] * pb[i])
        i += 1

_pfn_mul_uint32 = <size_t> _mul_uint32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_uint32_const(void *a, uint32_t c, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] * c)
        i += 1


_pfn_mul_uint32_const = <size_t> _mul_uint32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_uint32(void *a, void *b, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] / pb[i])
        i += 1

_pfn_div_uint32 = <size_t> _div_uint32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_uint32_const(void *a, uint32_t c, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] / c)
        i += 1


_pfn_div_uint32_const = <size_t> _div_uint32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_uint32(void *a, void *b, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] % pb[i])
        i += 1

_pfn_mod_uint32 = <size_t> _mod_uint32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_uint32_const(void *a, uint32_t c, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] % c)
        i += 1


_pfn_mod_uint32_const = <size_t> _mod_uint32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_uint32(void *a, void *b, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] & pb[i])
        i += 1

_pfn_and_uint32 = <size_t> _and_uint32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_uint32_const(void *a, uint32_t c, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] & c)
        i += 1


_pfn_and_uint32_const = <size_t> _and_uint32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_uint32(void *a, void *b, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] | pb[i])
        i += 1

_pfn_or_uint32 = <size_t> _or_uint32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_uint32_const(void *a, uint32_t c, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] | c)
        i += 1


_pfn_or_uint32_const = <size_t> _or_uint32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_uint32(void *a, void *b, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pb = <uint32_t *> b
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] ^ pb[i])
        i += 1

_pfn_xor_uint32 = <size_t> _xor_uint32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_uint32_const(void *a, uint32_t c, void *d, size_t l) nogil:
    cdef uint32_t *pa = <uint32_t *> a
    cdef uint32_t *pd = <uint32_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint32_t> (pa[i] ^ c)
        i += 1


_pfn_xor_uint32_const = <size_t> _xor_uint32_const




ctypedef void (*pfn_op_uint64_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_uint64_const_t) (void *a, uint64_t c, void *d, size_t l) nogil


cpdef op_uint64_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_uint64_t pfn = <pfn_op_uint64_t> <size_t> fn
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    pfn(pa, pb, pd, l)


cpdef op_uint64(fn, a, b, d, l):
    cdef pfn_op_uint64_t pfn = <pfn_op_uint64_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_uint64_const_raw(size_t fn, size_t a, uint64_t c, size_t d, size_t l):
    cdef pfn_op_uint64_const_t pfn = <pfn_op_uint64_const_t> <size_t> fn
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    pfn(pa, c, pd, l)


cpdef op_uint64_const(fn, a, c, d, l):
    cdef pfn_op_uint64_const_t pfn = <pfn_op_uint64_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef uint64_t cc = <uint64_t> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_uint64(void *a, void *b, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] + pb[i])
        i += 1

_pfn_add_uint64 = <size_t> _add_uint64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_uint64_const(void *a, uint64_t c, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] + c)
        i += 1


_pfn_add_uint64_const = <size_t> _add_uint64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_uint64(void *a, void *b, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] - pb[i])
        i += 1

_pfn_sub_uint64 = <size_t> _sub_uint64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_uint64_const(void *a, uint64_t c, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] - c)
        i += 1


_pfn_sub_uint64_const = <size_t> _sub_uint64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_uint64(void *a, void *b, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] * pb[i])
        i += 1

_pfn_mul_uint64 = <size_t> _mul_uint64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_uint64_const(void *a, uint64_t c, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] * c)
        i += 1


_pfn_mul_uint64_const = <size_t> _mul_uint64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_uint64(void *a, void *b, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] / pb[i])
        i += 1

_pfn_div_uint64 = <size_t> _div_uint64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_uint64_const(void *a, uint64_t c, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] / c)
        i += 1


_pfn_div_uint64_const = <size_t> _div_uint64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_uint64(void *a, void *b, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] % pb[i])
        i += 1

_pfn_mod_uint64 = <size_t> _mod_uint64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_uint64_const(void *a, uint64_t c, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] % c)
        i += 1


_pfn_mod_uint64_const = <size_t> _mod_uint64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_uint64(void *a, void *b, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] & pb[i])
        i += 1

_pfn_and_uint64 = <size_t> _and_uint64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _and_uint64_const(void *a, uint64_t c, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] & c)
        i += 1


_pfn_and_uint64_const = <size_t> _and_uint64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_uint64(void *a, void *b, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] | pb[i])
        i += 1

_pfn_or_uint64 = <size_t> _or_uint64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _or_uint64_const(void *a, uint64_t c, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] | c)
        i += 1


_pfn_or_uint64_const = <size_t> _or_uint64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_uint64(void *a, void *b, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pb = <uint64_t *> b
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] ^ pb[i])
        i += 1

_pfn_xor_uint64 = <size_t> _xor_uint64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _xor_uint64_const(void *a, uint64_t c, void *d, size_t l) nogil:
    cdef uint64_t *pa = <uint64_t *> a
    cdef uint64_t *pd = <uint64_t *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <uint64_t> (pa[i] ^ c)
        i += 1


_pfn_xor_uint64_const = <size_t> _xor_uint64_const




ctypedef void (*pfn_op_float32_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_float32_const_t) (void *a, float c, void *d, size_t l) nogil


cpdef op_float32_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_float32_t pfn = <pfn_op_float32_t> <size_t> fn
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    pfn(pa, pb, pd, l)


cpdef op_float32(fn, a, b, d, l):
    cdef pfn_op_float32_t pfn = <pfn_op_float32_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_float32_const_raw(size_t fn, size_t a, float c, size_t d, size_t l):
    cdef pfn_op_float32_const_t pfn = <pfn_op_float32_const_t> <size_t> fn
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    pfn(pa, c, pd, l)


cpdef op_float32_const(fn, a, c, d, l):
    cdef pfn_op_float32_const_t pfn = <pfn_op_float32_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef float cc = <float> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_float32(void *a, void *b, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] + pb[i])
        i += 1

_pfn_add_float32 = <size_t> _add_float32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_float32_const(void *a, float c, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] + c)
        i += 1


_pfn_add_float32_const = <size_t> _add_float32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_float32(void *a, void *b, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] - pb[i])
        i += 1

_pfn_sub_float32 = <size_t> _sub_float32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_float32_const(void *a, float c, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] - c)
        i += 1


_pfn_sub_float32_const = <size_t> _sub_float32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_float32(void *a, void *b, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] * pb[i])
        i += 1

_pfn_mul_float32 = <size_t> _mul_float32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_float32_const(void *a, float c, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] * c)
        i += 1


_pfn_mul_float32_const = <size_t> _mul_float32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_float32(void *a, void *b, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] / pb[i])
        i += 1

_pfn_div_float32 = <size_t> _div_float32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_float32_const(void *a, float c, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] / c)
        i += 1


_pfn_div_float32_const = <size_t> _div_float32_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_float32(void *a, void *b, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pb = <float *> b
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] % pb[i])
        i += 1

_pfn_mod_float32 = <size_t> _mod_float32



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_float32_const(void *a, float c, void *d, size_t l) nogil:
    cdef float *pa = <float *> a
    cdef float *pd = <float *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <float> (pa[i] % c)
        i += 1


_pfn_mod_float32_const = <size_t> _mod_float32_const




ctypedef void (*pfn_op_float64_t) (void *a, void *b, void *d, size_t l) nogil
ctypedef void (*pfn_op_float64_const_t) (void *a, double c, void *d, size_t l) nogil


cpdef op_float64_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
    cdef pfn_op_float64_t pfn = <pfn_op_float64_t> <size_t> fn
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    pfn(pa, pb, pd, l)


cpdef op_float64(fn, a, b, d, l):
    cdef pfn_op_float64_t pfn = <pfn_op_float64_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef BufferView bb = BufferView(b)
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)


cpdef op_float64_const_raw(size_t fn, size_t a, double c, size_t d, size_t l):
    cdef pfn_op_float64_const_t pfn = <pfn_op_float64_const_t> <size_t> fn
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    pfn(pa, c, pd, l)


cpdef op_float64_const(fn, a, c, d, l):
    cdef pfn_op_float64_const_t pfn = <pfn_op_float64_const_t> <size_t> fn
    cdef BufferView ba = BufferView(a)
    cdef double cc = <double> c
    cdef BufferView bd = BufferView(d)
    pfn(ba.buf.buf, cc, bd.buf.buf, l)





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_float64(void *a, void *b, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] + pb[i])
        i += 1

_pfn_add_float64 = <size_t> _add_float64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _add_float64_const(void *a, double c, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] + c)
        i += 1


_pfn_add_float64_const = <size_t> _add_float64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_float64(void *a, void *b, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] - pb[i])
        i += 1

_pfn_sub_float64 = <size_t> _sub_float64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _sub_float64_const(void *a, double c, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] - c)
        i += 1


_pfn_sub_float64_const = <size_t> _sub_float64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_float64(void *a, void *b, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] * pb[i])
        i += 1

_pfn_mul_float64 = <size_t> _mul_float64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mul_float64_const(void *a, double c, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] * c)
        i += 1


_pfn_mul_float64_const = <size_t> _mul_float64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_float64(void *a, void *b, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] / pb[i])
        i += 1

_pfn_div_float64 = <size_t> _div_float64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _div_float64_const(void *a, double c, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] / c)
        i += 1


_pfn_div_float64_const = <size_t> _div_float64_const





@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_float64(void *a, void *b, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pb = <double *> b
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] % pb[i])
        i += 1

_pfn_mod_float64 = <size_t> _mod_float64



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)

cdef void _mod_float64_const(void *a, double c, void *d, size_t l) nogil:
    cdef double *pa = <double *> a
    cdef double *pd = <double *> d
    cdef size_t i = 0
    while i < l:
        pd[i] = <double> (pa[i] % c)
        i += 1


_pfn_mod_float64_const = <size_t> _mod_float64_const




# cdef extern from "math.h":
#     float       fmaf(float x, float y, float z)
#     double      fma(double x, double y, double z)
#     long double fmal(long double x, long double y, long double z)
#
#
# % for (typ_nm, typ_s), fn_nam in zip(float_typ_pairs, ['fmaf', 'fma']):
#
#
# \{cy_opt_decos()}
# cdef void _fma_\{typ_nam}(void *a, void *b, void *d, size_t l) nogil:
#     cdef \{typ_s} *pa = <\{typ_s} *> a
#     cdef \{typ_s} *pb = <\{typ_s} *> b
#     cdef \{typ_s} *pd = <\{typ_s} *> d
#     cdef size_t i = 0
#     while i < l:
#         pd[i] = <\{typ_s}> \{fn_nam}(pa[i], pb[i])
#         i += 1
#
# _pfn_fma_\{typ_nam} = <size_t> _fma_\{typ_nam}
#
#
# \{cy_opt_decos()}
# cdef void _fma_\{typ_nam}_const(void *a, \{typ_s} c, void *d, size_t l) nogil:
#     cdef \{typ_s} *pa = <\{typ_s} *> a
#     cdef \{typ_s} *pd = <\{typ_s} *> d
#     cdef size_t i = 0
#     while i < l:
#         pd[i] = <\{typ_s}> \{fn_nam}(pa[i], c)
#         i += 1
#
#
# _pfn_fma_\{typ_nam}_const = <size_t> _fma_\{typ_nam}_const
#
#
# % endfor
