cimport cython

from ._vmath2 cimport *

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef void _op_add_sz_pi8_pi8_pi8(OpArg *args) nogil:
    cdef size_t a0 = args[0].sz
    cdef int8_t *a1 = <int8_t *> args[1].p
    cdef int8_t *a2 = <int8_t *> args[2].p
    cdef int8_t *a3 = <int8_t *> args[3].p
    cdef size_t i = 0
    while i < a0:
        a1[i] = <int8_t> (a2[i] + a3[i])
        i += 1

_pfn_op_add_sz_pf32_pf32_pf32 = <size_t> _op_add_sz_pf32_pf32_pf32

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef void _op_add_sz_pf32_pf32_pf32(OpArg *args) nogil:
    cdef size_t a0 = args[0].sz
    cdef float *a1 = <float *> args[1].p
    cdef float *a2 = <float *> args[2].p
    cdef float *a3 = <float *> args[3].p
    cdef size_t i = 0
    while i < a0:
        a1[i] = <float> (a2[i] + a3[i])
        i += 1

_pfn_op_add_sz_pi8_pi8_pi8 = <size_t> _op_add_sz_pi8_pi8_pi8
