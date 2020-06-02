<%doc>
TODO:

 - cy helpers:
  - bytes
  - objects

 - py wrappers:
  - Bytes to str (+ memoryviews?)
  - bitcasting float/double
  - uints?
  - abusing int32/64 as void*

 - dtypes:
  - object
  - float32/64?
  - string?

 - containers:
  - array
  - deque
  - forward_list
  - list
  - stack
  - queue
  - priority_queue
  - multiset
  - multimap
  - unordered_multiset
  - unordered_multimap
  - bitset

https://github.com/sagemath/sage/blob/cf9673bc59b43f791747b8ff31c5f072eeab88eb/src/sage/structure/coerce_dict.pyx
https://cython.readthedocs.io/en/latest/src/userguide/wrapping_CPlusPlus.html#wrapping-cplusplus
https://www.nexedi.com/blog/NXD-Document.Blog.Cypclass
https://cython.readthedocs.io/en/latest/src/userguide/wrapping_CPlusPlus.html
https://github.com/cython/cython/wiki/WrappingSetOfCppClasses
https://tillahoffmann.github.io/2016/04/18/Cpp-containers-in-cython.html
https://stackoverflow.com/questions/6684573/floating-point-keys-in-stdmap - ordered/lower_bound only?
</%doc>
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
        # ('Object', 'pPyObject', 'object'),
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