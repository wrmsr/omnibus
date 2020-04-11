from libc.stdint cimport uint64_t


cdef uint64_t MAX_UINT16 = 0xffff
cdef uint64_t MAX_UINT64 = 0xffffffffffffffff

cdef uint64_t _FNV_OFFSET = 0xcbf29ce484222325
cdef uint64_t _FNV_PRIME = 0x100000001b3


cdef uint64_t fnv1a_64(bytes data):
    hsh = _FNV_OFFSET
    for c in data:
        hsh ^= c
        hsh *= _FNV_PRIME
        hsh &= MAX_UINT64
    return hsh


cdef class Chd:

    cdef public list r  # uint64_t
    cdef public list indices  # uint16_t
    cdef public list keys  # bytes
    cdef public list values  # bytes

    def __init__(
            self,
            list r,
            list indices,
            list keys,
            list values,
    ):
        self.r = r
        self.indices = indices
        self.keys = keys
        self.values = values

    cpdef bytes get(self, bytes key):
        r0 = self.r[0]
        h = fnv1a_64(key) ^ r0
        i = h % len(self.indices)
        ri = self.indices[i]
        if ri >= len(self.r) & MAX_UINT16:
            # This can occur if there were unassigned slots in the hash table.
            return None
        r = self.r[ri]
        ti = (h ^ r) % len(self.keys)
        k = self.keys[ti]
        if k != key:
            return None
        v = self.values[ti]
        return v
