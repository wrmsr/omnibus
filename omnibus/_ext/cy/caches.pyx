from libcpp cimport bool


cdef class LruCacheLink:
    cdef public int seq
    cdef public object ins_prev
    cdef public object ins_next
    cdef public object lru_prev
    cdef public object lru_next
    cdef public object key
    cdef public object value
    cdef public float weight
    cdef public float written
    cdef public float accessed
    cdef public bool unlinked

    def __repr__(self):
        return (
            f'Link@{str(self.seq)}('
            f'ins_prev={("@" + str(self.ins_prev.seq)) if self.ins_prev is not None else None}, '
            f'ins_next={("@" + str(self.ins_next.seq)) if self.ins_next is not None else None}, '
            f'lru_prev={("@" + str(self.lru_prev.seq)) if self.lru_prev is not None else None}, '
            f'lru_next={("@" + str(self.lru_next.seq)) if self.lru_next is not None else None}, '
            f'key={self.key!r}, '
            f'value={self.value!r}, '
            f'weight={self.weight}, '
            f'written={self.written}, '
            f'accessed={self.accessed}, '
            f'unlinked={self.unlinked})'
        )
