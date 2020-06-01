from libc.stdint cimport int32_t
from libc.stdint cimport int64_t
from libc.stdint cimport int8_t
from libc.stdint cimport uint8_t

from libcpp.string cimport string

from cpython.bytes cimport PyBytes_AsString
from cpython.ref cimport Py_DECREF
from cpython.ref cimport Py_INCREF

from cython.operator cimport dereference as deref
from cython.operator cimport preincrement as preinc

from libcpp.vector cimport vector as cpp_vector
ctypedef cpp_vector[uint8_t] uint8_vector;


cdef extern from "helpers.hpp" namespace "stl_helpers":
    cdef cppclass Uint8VectorHash:
        pass


<%
    int_tups = [
        ('Int8', 'int8_t', 'int8_t'),
        ('Int32', 'int32_t', 'int32_t'),
        ('Int64', 'int64_t', 'int64_t'),
    ]

    extra_tups = [
        # ('String', 'string', 'string'),
        ('Bytes', 'uint8_vector', 'bytes'),
    ]

    all_tups = int_tups + extra_tups
%>


% for vprefix, vtype, vpytype in all_tups:

<%include file="stl_set.pyx.mako" args="vprefix=vprefix, vtype=vtype"/>
<%include file="stl_unordered_set.pyx.mako" args="vprefix=vprefix, vtype=vtype"/>
<%include file="stl_vector.pyx.mako" args="vprefix=vprefix, vtype=vtype, vpytype=vpytype"/>

% endfor

% for kprefix, ktype, kpytype in all_tups:
<% vprefix, vtype, vpytype = kprefix, ktype, kpytype %>

<%include file="stl_map.pyx.mako" args="kprefix=kprefix, ktype=ktype, vprefix=vprefix, vtype=vtype"/>
<%include file="stl_unordered_map.pyx.mako" args="kprefix=kprefix, ktype=ktype, vprefix=vprefix, vtype=vtype"/>

% endfor
