import ctypes as ct
import sys


class PyObject(ct.Structure):
    pass


if hasattr(sys, 'getobjects'):
    PyObject._fields_ = [
        # struct _object *_ob_next;
        ('_ob_next', ct.POINTER(PyObject)),
        # struct _object *_ob_prev;
        ('_ob_prev', ct.POINTER(PyObject)),
        # Py_refcnt_t ob_refcnt;
        ('ob_refcnt', ct.c_ssize_t),
        # struct _typeobject *ob_type;
        ('ob_type', ct.c_void_p),
    ]

else:
    PyObject._fields_ = [
        # Py_refcnt_t ob_refcnt;
        ('ob_refcnt', ct.c_ssize_t),
        # struct _typeobject *ob_type;
        ('ob_type', ct.c_void_p),
    ]


class PyVarObject(ct.Structure):
    pass


PyVarObject._fields_ = [
    # PyObject ob_base;
    ('ob_base', PyObject),
    # Py_ssize_t ob_size; /* Number of items in variable part */
    ('ob_size', ct.c_ssize_t),
]


class PyFrameObject(ct.Structure):
    pass


PyFrameObject._fields_ = [
    # PyObject_VAR_HEAD
    ('ob_base', PyVarObject),
    # struct _frame *f_back;      /* previous frame, or NULL */
    ('f_back', ct.POINTER(PyFrameObject)),
    # PyCodeObject *f_code;       /* code segment */
    ('f_code', ct.c_void_p),
    # PyObject *f_builtins;       /* builtin symbol table (PyDictObject) */
    ('f_builtins', ct.py_object),
    # PyObject *f_globals;        /* global symbol table (PyDictObject) */
    ('f_globals', ct.py_object),
    # PyObject *f_locals;         /* local symbol table (any mapping) */
    ('f_locals', ct.py_object),
    # PyObject **f_valuestack;    /* points after the last local */
    ('f_valuestack', ct.POINTER(ct.py_object)),
    # PyObject **f_stacktop;
    ('f_stacktop', ct.POINTER(ct.py_object)),
    # PyObject *f_trace;          /* Trace function */
    ('f_trace', ct.py_object),
    # char f_trace_lines;         /* Emit per-line trace events? */
    ('f_trace_lines', ct.c_char),
    # char f_trace_opcodes;       /* Emit per-opcode trace events? */
    ('f_trace_opcodes', ct.c_char),

    # PyObject *f_gen;
    ('f_gen', ct.py_object),

    # int f_lasti;                /* Last instruction if called */
    ('f_lasti', ct.c_int),
    # int f_lineno;               /* Current line number */
    ('f_lineno', ct.c_int),
    # int f_iblock;               /* index in f_blockstack */
    ('f_iblock', ct.c_int),
    # char f_executing;           /* whether the frame is still executing */
    ('f_executing', ct.c_char),
    # PyTryBlock f_blockstack[CO_MAXBLOCKS]; /* for try and loop blocks */
    ('f_blockstack', ct.c_void_p),
    # PyObject *f_localsplus[1];  /* locals+stack, dynamically sized */
    ('f_localsplus', ct.POINTER(ct.py_object)),
]
