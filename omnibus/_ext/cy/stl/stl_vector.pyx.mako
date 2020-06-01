<%page args="vprefix, vtype, vpytype"/>

from libcpp.vector cimport vector as cpp_vector


cdef class ${vprefix}Vector:

    <% _type = f'cpp_vector[{vtype}]' %>

    cdef ${_type} *v

    def __cinit__(self):
        self.v = new ${_type}()

    def __dealloc__(self):
        del self.v

    def __iter__(self):
        cdef ${_type}.iterator it = self.v.begin()
        while it != self.v.end():
            yield deref(it)
            preinc(it)

    def __reversed__(self):
        cdef ${_type}.reverse_iterator it = self.v.rbegin()
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

    def append(self, ${vpytype} value):
        %if vprefix == 'Bytes':
            cdef uint8_t *pval = <uint8_t*>PyBytes_AsString(value)
            cdef size_t vallen = len(value)
            cdef uint8_vector cval;
            cval.assign(pval, pval + vallen)
        %else:
            self.v.push_back(value)
        %endif

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
