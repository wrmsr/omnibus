import io
import textwrap


int_szs = [8, 16, 32, 64]
int_typs = [f'{p}int{sz}' for p in ['', 'u'] for sz in int_szs]

float_typ_pairs = [
    ('float32', 'float'),
    ('float64', 'double'),
]

typ_tups = [
    *[(t, t + '_t', True) for t in int_typs],
    *[(a, b, False) for a, b in float_typ_pairs],
]

com_op_tups = [
    ('add', '+'),
    ('sub', '-'),
    ('mul', '*'),
    ('div', '/'),
    ('mod', '%'),
]

int_op_tups = [
    ('and', '&'),
    ('or', '|'),
    ('xor', '^'),
]

cy_opt_decos = """
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
""".strip()


def _main():
    buf = io.StringIO()

    def _emit(s):
        ls = s.splitlines()
        ps = [
            p
            for l in ls
            if l and not l.startswith('@')
            for p in [next((i for i, c in enumerate(l) if c != ' '), None)]
            if p is not None
        ]
        i = min(ps) if ps else 0
        s = '\n'.join((' ' * i + l) if not l.startswith(' ') else l for l in ls).rstrip()
        buf.write(textwrap.dedent(s))
        buf.write('\n')

    _emit(f"""
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
    """)

    _emit('')
    _emit('\n'.join(f"""
    from libc.stdint cimport {typ}_t
    """.strip() for typ in int_typs))

    for typ_nam, typ_s, typ_is_int in typ_tups:
        _emit(f"""
        ctypedef void (*pfn_op_{typ_nam}_t) (void *a, void *b, void *d, size_t l) nogil
        ctypedef void (*pfn_op_{typ_nam}_const_t) (void *a, {typ_s} c, void *d, size_t l) nogil

        cpdef op_{typ_nam}_raw(size_t fn, size_t a, size_t b, size_t d, size_t l):
            cdef pfn_op_{typ_nam}_t pfn = <pfn_op_{typ_nam}_t> <size_t> fn
            cdef {typ_s} *pa = <{typ_s} *> a
            cdef {typ_s} *pb = <{typ_s} *> b
            cdef {typ_s} *pd = <{typ_s} *> d
            pfn(pa, pb, pd, l)

        cpdef op_{typ_nam}(fn, a, b, d, l):
            cdef pfn_op_{typ_nam}_t pfn = <pfn_op_{typ_nam}_t> <size_t> fn
            cdef BufferView ba = BufferView(a)
            cdef BufferView bb = BufferView(b)
            cdef BufferView bd = BufferView(d)
            pfn(ba.buf.buf, bb.buf.buf, bd.buf.buf, l)

        cpdef op_{typ_nam}_const_raw(size_t fn, size_t a, {typ_s} c, size_t d, size_t l):
            cdef pfn_op_{typ_nam}_const_t pfn = <pfn_op_{typ_nam}_const_t> <size_t> fn
            cdef {typ_s} *pa = <{typ_s} *> a
            cdef {typ_s} *pd = <{typ_s} *> d
            pfn(pa, c, pd, l)

        cpdef op_{typ_nam}_const(fn, a, c, d, l):
            cdef pfn_op_{typ_nam}_const_t pfn = <pfn_op_{typ_nam}_const_t> <size_t> fn
            cdef BufferView ba = BufferView(a)
            cdef {typ_s} cc = <{typ_s}> c
            cdef BufferView bd = BufferView(d)
            pfn(ba.buf.buf, cc, bd.buf.buf, l)
        """)

        for op_nam, op_s in (com_op_tups + (int_op_tups if typ_is_int else [])):
            _emit(f"""
            {cy_opt_decos}
            cdef void _{op_nam}_{typ_nam}(void *a, void *b, void *d, size_t l) nogil:
                cdef {typ_s} *pa = <{typ_s} *> a
                cdef {typ_s} *pb = <{typ_s} *> b
                cdef {typ_s} *pd = <{typ_s} *> d
                cdef size_t i = 0
                while i < l:
                    pd[i] = <{typ_s}> (pa[i] {op_s} pb[i])
                    i += 1

            _pfn_{op_nam}_{typ_nam} = <size_t> _{op_nam}_{typ_nam}

            {cy_opt_decos}
            cdef void _{op_nam}_{typ_nam}_const(void *a, {typ_s} c, void *d, size_t l) nogil:
                cdef {typ_s} *pa = <{typ_s} *> a
                cdef {typ_s} *pd = <{typ_s} *> d
                cdef size_t i = 0
                while i < l:
                    pd[i] = <{typ_s}> (pa[i] {op_s} c)
                    i += 1

            _pfn_{op_nam}_{typ_nam}_const = <size_t> _{op_nam}_{typ_nam}_const
            """)

    _emit(f"""
    cdef extern from "math.h":
        float       fmaf(float x, float y, float z) nogil
        double      fma(double x, double y, double z) nogil
        long double fmal(long double x, long double y, long double z) nogil
    """)

    for (typ_nm, typ_s), fn_nm in zip(float_typ_pairs, ['fmaf', 'fma']):
        _emit(f"""
        {cy_opt_decos}
        cdef void _fma_{typ_nm}(void *a, void *b, void *c, void *d, size_t l) nogil:
            cdef {typ_s} *pa = <{typ_s} *> a
            cdef {typ_s} *pb = <{typ_s} *> b
            cdef {typ_s} *pc = <{typ_s} *> c
            cdef {typ_s} *pd = <{typ_s} *> d
            cdef size_t i = 0
            while i < l:
                pd[i] = <{typ_s}> {fn_nm}(pa[i], pb[i], pc[i])
                i += 1

        _pfn_fma_{typ_nm} = <size_t> _fma_{typ_nm}

        {cy_opt_decos}
        cdef void _fma_{typ_nm}_mconst(void *a, {typ_s} b, void *c, void *d, size_t l) nogil:
            cdef {typ_s} *pa = <{typ_s} *> a
            cdef {typ_s} *pc = <{typ_s} *> c
            cdef {typ_s} *pd = <{typ_s} *> d
            cdef size_t i = 0
            while i < l:
                pd[i] = <{typ_s}> {fn_nm}(pa[i], b, pc[i])
                i += 1

        _pfn_fma_{typ_nm}_mconst = <size_t> _fma_{typ_nm}_mconst

        {cy_opt_decos}
        cdef void _fma_{typ_nm}_aconst(void *a, void *b, {typ_s} c, void *d, size_t l) nogil:
            cdef {typ_s} *pa = <{typ_s} *> a
            cdef {typ_s} *pb = <{typ_s} *> b
            cdef {typ_s} *pd = <{typ_s} *> d
            cdef size_t i = 0
            while i < l:
                pd[i] = <{typ_s}> {fn_nm}(pa[i], pb[i], c)
                i += 1

        _pfn_fma_{typ_nm}_aconst = <size_t> _fma_{typ_nm}_aconst

        {cy_opt_decos}
        cdef void _fma_{typ_nm}_mconst_aconst(void *a, {typ_s} b, {typ_s} c, void *d, size_t l) nogil:
            cdef {typ_s} *pa = <{typ_s} *> a
            cdef {typ_s} *pd = <{typ_s} *> d
            cdef size_t i = 0
            while i < l:
                pd[i] = <{typ_s}> {fn_nm}(pa[i], b, c)
                i += 1

        _pfn_fma_{typ_nm}_mconst_aconst = <size_t> _fma_{typ_nm}_mconst_aconst
        """)

    for typ_nm, typ_s in float_typ_pairs:
        _emit(f"""
        {cy_opt_decos}
        cdef void _mm_{typ_nm}(void *a, void *b, void *d, size_t n, size_t m, size_t p) nogil:
            cdef {typ_s} *pa = <{typ_s} *> a
            cdef {typ_s} *pb = <{typ_s} *> b
            cdef {typ_s} *pd = <{typ_s} *> d
            cdef size_t i = 0
            cdef size_t j = 0
            cdef size_t k = 0
            cdef {typ_s} tmp = 0.0
            while i < n:
                j = 0
                while j < p:
                    tmp = 0.0
                    k = 0
                    while k < m:
                        tmp += pa[i*m+k] * pb[k*m+j]
                        k += 1
                    pd[i*m+j] = tmp
                    j += 1
                i += 1

        _pfn_mm_{typ_nm} = <size_t> _mm_{typ_nm}
        """)

    print(buf.getvalue())


if __name__ == '__main__':
    _main()
