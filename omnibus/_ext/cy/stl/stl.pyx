
from libc.stdint cimport int32_t
from libc.stdint cimport int64_t
from libc.stdint cimport int8_t
from libc.stdint cimport uint8_t

from libcpp.string cimport string

from cpython.bytes cimport PyBytes_AsString
from cpython.ref cimport Py_DECREF
from cpython.ref cimport Py_INCREF
from cpython cimport PyObject

from cython.operator cimport dereference as deref
from cython.operator cimport preincrement as preinc

from libcpp.vector cimport vector as cpp_vector

ctypedef cpp_vector[uint8_t] uint8_vector
ctypedef PyObject* pPyobject


cdef extern from "helpers.h" namespace "stl_helpers":
    cdef cppclass Uint8VectorHash:
        pass








from libcpp.set cimport set as cpp_set


cdef class Int8Set:

    

    cdef cpp_set[int8_t] *s;

    def __cinit__(self):
        self.s = new cpp_set[int8_t]()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef cpp_set[int8_t].iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef cpp_set[int8_t].reverse_iterator it = self.s.rbegin()
        while it != self.s.rend():
            yield deref(it)
            preinc(it)

    def __len__(self):
        return self.s.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def isdisjoint(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def discard(self, value):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __ior__(self, it):
        raise NotImplementedError

    def __iand__(self, it):
        raise NotImplementedError

    def __ixor__(self, it):
        raise NotImplementedError

    def __isub__(self, it):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def find(self, value):
        raise NotImplementedError

    def iter(self, base=None):
        raise NotImplementedError

    def riter(self, base=None):
        raise NotImplementedError



from libcpp.unordered_set cimport unordered_set as cpp_unordered_set


cdef class Int8UnorderedSet:

    

    cdef cpp_unordered_set[int8_t] *s;

    def __cinit__(self):
        self.s = new cpp_unordered_set[int8_t]()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef cpp_unordered_set[int8_t].iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        raise TypeError

    def __len__(self):
        return self.s.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def isdisjoint(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def discard(self, value):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __ior__(self, it):
        raise NotImplementedError

    def __iand__(self, it):
        raise NotImplementedError

    def __ixor__(self, it):
        raise NotImplementedError

    def __isub__(self, it):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError



from libcpp.vector cimport vector as cpp_vector


cdef class Int8Vector:

    

    cdef cpp_vector[int8_t] *v

    def __cinit__(self):
        self.v = new cpp_vector[int8_t]()

    def __dealloc__(self):
        del self.v

    def __iter__(self):
        cdef cpp_vector[int8_t].iterator it = self.v.begin()
        while it != self.v.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef cpp_vector[int8_t].reverse_iterator it = self.v.rbegin()
        while it != self.v.rend():
            yield deref(it)
            preinc(it)

    def __len__(self):
        return self.v.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def index(self, value, start=0, stop=None):
        raise NotImplementedError

    def count(self, value):
        raise NotImplementedError

    def __setitem__(self, index, value):
        raise NotImplementedError

    def __delitem__(self, index):
        raise NotImplementedError

    def insert(self, index, value):
        raise NotImplementedError

    def append(self, int8_t value):
            self.v.push_back(value)

    def clear(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def extend(self, values):
        raise NotImplementedError

    def pop(self, index=-1):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def __iadd__(self, values):
        raise NotImplementedError





from libcpp.set cimport set as cpp_set


cdef class Int32Set:

    

    cdef cpp_set[int32_t] *s;

    def __cinit__(self):
        self.s = new cpp_set[int32_t]()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef cpp_set[int32_t].iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef cpp_set[int32_t].reverse_iterator it = self.s.rbegin()
        while it != self.s.rend():
            yield deref(it)
            preinc(it)

    def __len__(self):
        return self.s.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def isdisjoint(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def discard(self, value):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __ior__(self, it):
        raise NotImplementedError

    def __iand__(self, it):
        raise NotImplementedError

    def __ixor__(self, it):
        raise NotImplementedError

    def __isub__(self, it):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def find(self, value):
        raise NotImplementedError

    def iter(self, base=None):
        raise NotImplementedError

    def riter(self, base=None):
        raise NotImplementedError



from libcpp.unordered_set cimport unordered_set as cpp_unordered_set


cdef class Int32UnorderedSet:

    

    cdef cpp_unordered_set[int32_t] *s;

    def __cinit__(self):
        self.s = new cpp_unordered_set[int32_t]()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef cpp_unordered_set[int32_t].iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        raise TypeError

    def __len__(self):
        return self.s.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def isdisjoint(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def discard(self, value):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __ior__(self, it):
        raise NotImplementedError

    def __iand__(self, it):
        raise NotImplementedError

    def __ixor__(self, it):
        raise NotImplementedError

    def __isub__(self, it):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError



from libcpp.vector cimport vector as cpp_vector


cdef class Int32Vector:

    

    cdef cpp_vector[int32_t] *v

    def __cinit__(self):
        self.v = new cpp_vector[int32_t]()

    def __dealloc__(self):
        del self.v

    def __iter__(self):
        cdef cpp_vector[int32_t].iterator it = self.v.begin()
        while it != self.v.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef cpp_vector[int32_t].reverse_iterator it = self.v.rbegin()
        while it != self.v.rend():
            yield deref(it)
            preinc(it)

    def __len__(self):
        return self.v.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def index(self, value, start=0, stop=None):
        raise NotImplementedError

    def count(self, value):
        raise NotImplementedError

    def __setitem__(self, index, value):
        raise NotImplementedError

    def __delitem__(self, index):
        raise NotImplementedError

    def insert(self, index, value):
        raise NotImplementedError

    def append(self, int32_t value):
            self.v.push_back(value)

    def clear(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def extend(self, values):
        raise NotImplementedError

    def pop(self, index=-1):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def __iadd__(self, values):
        raise NotImplementedError





from libcpp.set cimport set as cpp_set


cdef class Int64Set:

    

    cdef cpp_set[int64_t] *s;

    def __cinit__(self):
        self.s = new cpp_set[int64_t]()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef cpp_set[int64_t].iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef cpp_set[int64_t].reverse_iterator it = self.s.rbegin()
        while it != self.s.rend():
            yield deref(it)
            preinc(it)

    def __len__(self):
        return self.s.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def isdisjoint(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def discard(self, value):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __ior__(self, it):
        raise NotImplementedError

    def __iand__(self, it):
        raise NotImplementedError

    def __ixor__(self, it):
        raise NotImplementedError

    def __isub__(self, it):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def find(self, value):
        raise NotImplementedError

    def iter(self, base=None):
        raise NotImplementedError

    def riter(self, base=None):
        raise NotImplementedError



from libcpp.unordered_set cimport unordered_set as cpp_unordered_set


cdef class Int64UnorderedSet:

    

    cdef cpp_unordered_set[int64_t] *s;

    def __cinit__(self):
        self.s = new cpp_unordered_set[int64_t]()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef cpp_unordered_set[int64_t].iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        raise TypeError

    def __len__(self):
        return self.s.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def isdisjoint(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def discard(self, value):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __ior__(self, it):
        raise NotImplementedError

    def __iand__(self, it):
        raise NotImplementedError

    def __ixor__(self, it):
        raise NotImplementedError

    def __isub__(self, it):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError



from libcpp.vector cimport vector as cpp_vector


cdef class Int64Vector:

    

    cdef cpp_vector[int64_t] *v

    def __cinit__(self):
        self.v = new cpp_vector[int64_t]()

    def __dealloc__(self):
        del self.v

    def __iter__(self):
        cdef cpp_vector[int64_t].iterator it = self.v.begin()
        while it != self.v.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef cpp_vector[int64_t].reverse_iterator it = self.v.rbegin()
        while it != self.v.rend():
            yield deref(it)
            preinc(it)

    def __len__(self):
        return self.v.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def index(self, value, start=0, stop=None):
        raise NotImplementedError

    def count(self, value):
        raise NotImplementedError

    def __setitem__(self, index, value):
        raise NotImplementedError

    def __delitem__(self, index):
        raise NotImplementedError

    def insert(self, index, value):
        raise NotImplementedError

    def append(self, int64_t value):
            self.v.push_back(value)

    def clear(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def extend(self, values):
        raise NotImplementedError

    def pop(self, index=-1):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def __iadd__(self, values):
        raise NotImplementedError





from libcpp.set cimport set as cpp_set


cdef class BytesSet:

    

    cdef cpp_set[uint8_vector] *s;

    def __cinit__(self):
        self.s = new cpp_set[uint8_vector]()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef cpp_set[uint8_vector].iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef cpp_set[uint8_vector].reverse_iterator it = self.s.rbegin()
        while it != self.s.rend():
            yield deref(it)
            preinc(it)

    def __len__(self):
        return self.s.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def isdisjoint(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def discard(self, value):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __ior__(self, it):
        raise NotImplementedError

    def __iand__(self, it):
        raise NotImplementedError

    def __ixor__(self, it):
        raise NotImplementedError

    def __isub__(self, it):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def find(self, value):
        raise NotImplementedError

    def iter(self, base=None):
        raise NotImplementedError

    def riter(self, base=None):
        raise NotImplementedError



from libcpp.unordered_set cimport unordered_set as cpp_unordered_set


cdef class BytesUnorderedSet:

    

    cdef cpp_unordered_set[uint8_vector, Uint8VectorHash] *s;

    def __cinit__(self):
        self.s = new cpp_unordered_set[uint8_vector, Uint8VectorHash]()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef cpp_unordered_set[uint8_vector, Uint8VectorHash].iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        raise TypeError

    def __len__(self):
        return self.s.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def isdisjoint(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError

    def discard(self, value):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __ior__(self, it):
        raise NotImplementedError

    def __iand__(self, it):
        raise NotImplementedError

    def __ixor__(self, it):
        raise NotImplementedError

    def __isub__(self, it):
        raise NotImplementedError

    def add(self, value):
        raise NotImplementedError



from libcpp.vector cimport vector as cpp_vector


cdef class BytesVector:

    

    cdef cpp_vector[uint8_vector] *v

    def __cinit__(self):
        self.v = new cpp_vector[uint8_vector]()

    def __dealloc__(self):
        del self.v

    def __iter__(self):
        cdef cpp_vector[uint8_vector].iterator it = self.v.begin()
        while it != self.v.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef cpp_vector[uint8_vector].reverse_iterator it = self.v.rbegin()
        while it != self.v.rend():
            yield deref(it)
            preinc(it)

    def __len__(self):
        return self.v.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def index(self, value, start=0, stop=None):
        raise NotImplementedError

    def count(self, value):
        raise NotImplementedError

    def __setitem__(self, index, value):
        raise NotImplementedError

    def __delitem__(self, index):
        raise NotImplementedError

    def insert(self, index, value):
        raise NotImplementedError

    def append(self, bytes value):
            cdef uint8_t *pval = <uint8_t*>PyBytes_AsString(value)
            cdef size_t vallen = len(value)
            cdef uint8_vector cval;
            cval.assign(pval, pval + vallen)

    def clear(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def extend(self, values):
        raise NotImplementedError

    def pop(self, index=-1):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def __iadd__(self, values):
        raise NotImplementedError







from libcpp.map cimport map as cpp_map

from libcpp.utility cimport pair as cpp_pair


cdef class Int8Int8Map:

    

    cdef cpp_map[int8_t, int8_t] *m

    def __cinit__(self):
        self.m = new cpp_map[int8_t, int8_t]()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef cpp_map[int8_t, int8_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield deref(it).first
            preinc(it)

    def __reversed__(self):
        cdef cpp_map[int8_t, int8_t].reverse_iterator it = self.m.rbegin()
        while it != self.m.rend():
            yield deref(it).first
            preinc(it)

    def __len__(self):
        return self.m.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def items(self):
        cdef cpp_map[int8_t, int8_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, int8_t key, int8_t value):
        self.m.insert(cpp_pair[int8_t, int8_t](key, value))

    def __delitem__(self, key):
        raise NotImplementedError

    def pop(self, key, default=None):
        raise NotImplementedError

    def popitem(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, other=(), **kwds):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError

    def ritems(self):
        raise NotImplementedError

    def itemsfrom(self, key):
        raise NotImplementedError

    def ritemsfrom(self, key):
        raise NotImplementedError



from libcpp.unordered_map cimport unordered_map as cpp_unordered_map

from libcpp.utility cimport pair as cpp_pair


cdef class Int8Int8UnorderedMap:

    

    cdef cpp_unordered_map[int8_t, int8_t] *m

    def __cinit__(self):
        self.m = new cpp_unordered_map[int8_t, int8_t]()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef cpp_unordered_map[int8_t, int8_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield deref(it).first
            preinc(it)

    def __reversed__(self):
        raise TypeError

    def __len__(self):
        return self.m.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def items(self):
        cdef cpp_unordered_map[int8_t, int8_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, int8_t key, int8_t value):
        self.m.insert(cpp_pair[int8_t, int8_t](key, value))

    def __delitem__(self, key):
        raise NotImplementedError

    def pop(self, key, default=None):
        raise NotImplementedError

    def popitem(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, other=(), **kwds):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError






from libcpp.map cimport map as cpp_map

from libcpp.utility cimport pair as cpp_pair


cdef class Int32Int32Map:

    

    cdef cpp_map[int32_t, int32_t] *m

    def __cinit__(self):
        self.m = new cpp_map[int32_t, int32_t]()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef cpp_map[int32_t, int32_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield deref(it).first
            preinc(it)

    def __reversed__(self):
        cdef cpp_map[int32_t, int32_t].reverse_iterator it = self.m.rbegin()
        while it != self.m.rend():
            yield deref(it).first
            preinc(it)

    def __len__(self):
        return self.m.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def items(self):
        cdef cpp_map[int32_t, int32_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, int32_t key, int32_t value):
        self.m.insert(cpp_pair[int32_t, int32_t](key, value))

    def __delitem__(self, key):
        raise NotImplementedError

    def pop(self, key, default=None):
        raise NotImplementedError

    def popitem(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, other=(), **kwds):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError

    def ritems(self):
        raise NotImplementedError

    def itemsfrom(self, key):
        raise NotImplementedError

    def ritemsfrom(self, key):
        raise NotImplementedError



from libcpp.unordered_map cimport unordered_map as cpp_unordered_map

from libcpp.utility cimport pair as cpp_pair


cdef class Int32Int32UnorderedMap:

    

    cdef cpp_unordered_map[int32_t, int32_t] *m

    def __cinit__(self):
        self.m = new cpp_unordered_map[int32_t, int32_t]()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef cpp_unordered_map[int32_t, int32_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield deref(it).first
            preinc(it)

    def __reversed__(self):
        raise TypeError

    def __len__(self):
        return self.m.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def items(self):
        cdef cpp_unordered_map[int32_t, int32_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, int32_t key, int32_t value):
        self.m.insert(cpp_pair[int32_t, int32_t](key, value))

    def __delitem__(self, key):
        raise NotImplementedError

    def pop(self, key, default=None):
        raise NotImplementedError

    def popitem(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, other=(), **kwds):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError






from libcpp.map cimport map as cpp_map

from libcpp.utility cimport pair as cpp_pair


cdef class Int64Int64Map:

    

    cdef cpp_map[int64_t, int64_t] *m

    def __cinit__(self):
        self.m = new cpp_map[int64_t, int64_t]()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef cpp_map[int64_t, int64_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield deref(it).first
            preinc(it)

    def __reversed__(self):
        cdef cpp_map[int64_t, int64_t].reverse_iterator it = self.m.rbegin()
        while it != self.m.rend():
            yield deref(it).first
            preinc(it)

    def __len__(self):
        return self.m.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def items(self):
        cdef cpp_map[int64_t, int64_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, int64_t key, int64_t value):
        self.m.insert(cpp_pair[int64_t, int64_t](key, value))

    def __delitem__(self, key):
        raise NotImplementedError

    def pop(self, key, default=None):
        raise NotImplementedError

    def popitem(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, other=(), **kwds):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError

    def ritems(self):
        raise NotImplementedError

    def itemsfrom(self, key):
        raise NotImplementedError

    def ritemsfrom(self, key):
        raise NotImplementedError



from libcpp.unordered_map cimport unordered_map as cpp_unordered_map

from libcpp.utility cimport pair as cpp_pair


cdef class Int64Int64UnorderedMap:

    

    cdef cpp_unordered_map[int64_t, int64_t] *m

    def __cinit__(self):
        self.m = new cpp_unordered_map[int64_t, int64_t]()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef cpp_unordered_map[int64_t, int64_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield deref(it).first
            preinc(it)

    def __reversed__(self):
        raise TypeError

    def __len__(self):
        return self.m.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def items(self):
        cdef cpp_unordered_map[int64_t, int64_t].iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, int64_t key, int64_t value):
        self.m.insert(cpp_pair[int64_t, int64_t](key, value))

    def __delitem__(self, key):
        raise NotImplementedError

    def pop(self, key, default=None):
        raise NotImplementedError

    def popitem(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, other=(), **kwds):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError






from libcpp.map cimport map as cpp_map

from libcpp.utility cimport pair as cpp_pair


cdef class BytesBytesMap:

    

    cdef cpp_map[uint8_vector, uint8_vector] *m

    def __cinit__(self):
        self.m = new cpp_map[uint8_vector, uint8_vector]()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef cpp_map[uint8_vector, uint8_vector].iterator it = self.m.begin()
        while it != self.m.end():
            yield deref(it).first
            preinc(it)

    def __reversed__(self):
        cdef cpp_map[uint8_vector, uint8_vector].reverse_iterator it = self.m.rbegin()
        while it != self.m.rend():
            yield deref(it).first
            preinc(it)

    def __len__(self):
        return self.m.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def items(self):
        cdef cpp_map[uint8_vector, uint8_vector].iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, uint8_vector key, uint8_vector value):
        self.m.insert(cpp_pair[uint8_vector, uint8_vector](key, value))

    def __delitem__(self, key):
        raise NotImplementedError

    def pop(self, key, default=None):
        raise NotImplementedError

    def popitem(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, other=(), **kwds):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError

    def ritems(self):
        raise NotImplementedError

    def itemsfrom(self, key):
        raise NotImplementedError

    def ritemsfrom(self, key):
        raise NotImplementedError



from libcpp.unordered_map cimport unordered_map as cpp_unordered_map

from libcpp.utility cimport pair as cpp_pair


cdef class BytesBytesUnorderedMap:

    

    cdef cpp_unordered_map[uint8_vector, uint8_vector, Uint8VectorHash] *m

    def __cinit__(self):
        self.m = new cpp_unordered_map[uint8_vector, uint8_vector, Uint8VectorHash]()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef cpp_unordered_map[uint8_vector, uint8_vector, Uint8VectorHash].iterator it = self.m.begin()
        while it != self.m.end():
            yield deref(it).first
            preinc(it)

    def __reversed__(self):
        raise TypeError

    def __len__(self):
        return self.m.size()

    def __contains__(self, x):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def items(self):
        cdef cpp_unordered_map[uint8_vector, uint8_vector, Uint8VectorHash].iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, uint8_vector key, uint8_vector value):
        self.m.insert(cpp_pair[uint8_vector, uint8_vector](key, value))

    def __delitem__(self, key):
        raise NotImplementedError

    def pop(self, key, default=None):
        raise NotImplementedError

    def popitem(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, other=(), **kwds):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError


