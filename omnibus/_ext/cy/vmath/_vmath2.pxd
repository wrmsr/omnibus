from libc.stdint cimport int8_t
from libc.stdint cimport int16_t
from libc.stdint cimport int32_t
from libc.stdint cimport int64_t
from libc.stdint cimport uint8_t
from libc.stdint cimport uint16_t
from libc.stdint cimport uint32_t
from libc.stdint cimport uint64_t

cdef union OpArg:
    size_t sz
    void *p

    int8_t i8
    int16_t i16
    int32_t i32
    int64_t i64

    uint8_t u8
    uint16_t u16
    uint32_t u32
    uint64_t u64

    float f32
    double f64

ctypedef void (*pfn_op_t) (OpArg *args) nogil
