<%page args="vprefix, vtype"/>

from libcpp.set cimport set as cpp_set


cdef class ${vprefix}Set:

    <% _type = f'cpp_set[{vtype}]' %>

    cdef ${_type} *s;

    def __cinit__(self):
        self.s = new ${_type}()

    def __dealloc__(self):
        del self.s

    def __iter__(self):
        cdef ${_type}.iterator it = self.s.begin()
        while it != self.s.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef ${_type}.reverse_iterator it = self.s.rbegin()
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
