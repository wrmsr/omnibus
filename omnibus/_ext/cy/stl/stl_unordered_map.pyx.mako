<%page args="kprefix, ktype, vprefix, vtype"/>

from .gen_unordered_map cimport unordered_map as cpp_unordered_map

from libcpp.utility cimport pair as cpp_pair


cdef class ${kprefix}${vprefix}UnorderedMap:

    <% _type = f'cpp_unordered_map[{vtype}, {vtype}{", Uint8VectorHash" if vprefix == "Bytes" else ""}]' %>

    cdef ${_type} *m

    def __cinit__(self):
        self.m = new ${_type}()

    def __dealloc__(self):
        del self.m

    def __iter__(self):
        cdef ${_type}.iterator it = self.m.begin()
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
        cdef ${_type}.iterator it = self.m.begin()
        while it != self.m.end():
            yield (deref(it).first, deref(it).second)
            preinc(it)

    def values(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __setitem__(self, ${ktype} key, ${vtype} value):
        self.m.insert(cpp_pair[${ktype}, ${vtype}](key, value))

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
