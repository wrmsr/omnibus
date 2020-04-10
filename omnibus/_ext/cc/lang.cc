#include <unistd.h>

#include <Python.h>
#include <structmember.h>


typedef struct {
    PyObject_HEAD
    PyObject *obj;
    PyObject *dict;
    PyObject *weakreflist; /* List of weak references */
} constantobject;

static PyObject *
constant_new(PyTypeObject *type, PyObject *args, PyObject *kw)
{
    PyObject *obj;
    constantobject *co;

    if (PyTuple_GET_SIZE(args) != 1) {
        PyErr_SetString(PyExc_TypeError, "type 'constant' takes exactly one argument");
        return NULL;
    }

    obj = PyTuple_GET_ITEM(args, 0);

    co = (constantobject *)type->tp_alloc(type, 0);
    if (co == NULL)
        return NULL;

    co->obj = obj;
    Py_INCREF(obj);

    return (PyObject *)co;
}

static void
constant_dealloc(constantobject *co)
{
    PyObject_GC_UnTrack(co);
    if (co->weakreflist != NULL)
        PyObject_ClearWeakRefs((PyObject *) co);
    Py_XDECREF(co->obj);
    Py_XDECREF(co->dict);
    Py_TYPE(co)->tp_free(co);
}

static PyObject *
constant_call(constantobject *co, PyObject *args, PyObject *kwargs)
{
    Py_INCREF(co->obj);
    return co->obj;
}

static int
constant_traverse(constantobject *co, visitproc visit, void *arg)
{
    Py_VISIT(co->obj);
    Py_VISIT(co->dict);
    return 0;
}

PyDoc_STRVAR(constant_doc, "constant(obj) - new function returning obj\n");

#define OFF(x) offsetof(constantobject, x)
static PyMemberDef constant_memberlist[] = {
    {"obj",            T_OBJECT,       OFF(obj),        READONLY, "object to return"},
    {NULL}  /* Sentinel */
};

static PyGetSetDef constant_getsetlist[] = {
    {"__dict__", PyObject_GenericGetDict, PyObject_GenericSetDict},
    {NULL} /* Sentinel */
};

static PyObject *
constant_repr(constantobject *co)
{
    PyObject *result = NULL;
    int status;

    status = Py_ReprEnter((PyObject *)co);
    if (status != 0) {
        if (status < 0)
            return NULL;
        return PyUnicode_FromString("...");
    }

    result = PyUnicode_FromFormat("%s(%R)", Py_TYPE(co)->tp_name, co->obj);

    Py_ReprLeave((PyObject *)co);
    return result;
}

/* Pickle strategy:
   __reduce__ by itself doesn't support getting kwargs in the unpickle
   operation so we define a __setstate__ that replaces all the information
   about the constant.  If we only replaced part of it someone would use
   it as a hook to do strange things.
 */

static PyObject *
constant_reduce(constantobject *co, PyObject *unused)
{
    return Py_BuildValue("O(O)(OO)", Py_TYPE(co), co->obj, co->obj, co->dict ? co->dict : Py_None);
}

static PyObject *
constant_setstate(constantobject *co, PyObject *state)
{
    PyObject *obj, *dict;

    if (!PyTuple_Check(state) ||
        !PyArg_ParseTuple(state, "OO", &obj, &dict))
    {
        PyErr_SetString(PyExc_TypeError, "invalid constant state");
        return NULL;
    }

    if (dict == Py_None)
        dict = NULL;
    else
        Py_INCREF(dict);

    Py_INCREF(obj);
    Py_SETREF(co->obj, obj);
    Py_XSETREF(co->dict, dict);
    Py_RETURN_NONE;
}

static PyMethodDef constant_methods[] = {
    {"__reduce__", (PyCFunction)constant_reduce, METH_NOARGS},
    {"__setstate__", (PyCFunction)constant_setstate, METH_O},
    {NULL,              NULL}           /* sentinel */
};

static PyTypeObject constant_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "constant",                /* tp_name */
    sizeof(constantobject),              /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)constant_dealloc,        /* tp_dealloc */
    0,                                  /* tp_vectorcall_offset */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_as_async */
    (reprfunc)constant_repr,             /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    (ternaryfunc)constant_call,          /* tp_call */
    0,                                  /* tp_str */
    PyObject_GenericGetAttr,            /* tp_getattro */
    PyObject_GenericSetAttr,            /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE,            /* tp_flags */
    constant_doc,                        /* tp_doc */
    (traverseproc)constant_traverse,     /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    offsetof(constantobject, weakreflist),       /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    0,                                  /* tp_iternext */
    constant_methods,                    /* tp_methods */
    constant_memberlist,                 /* tp_members */
    constant_getsetlist,                 /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    offsetof(constantobject, dict),      /* tp_dictoffset */
    0,                                  /* tp_init */
    0,                                  /* tp_alloc */
    constant_new,                        /* tp_new */
    PyObject_GC_Del,                    /* tp_free */
};


static PyMethodDef module_methods[] = {
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "lang",
    "omnibus c++ lang extension",
    -1,
    module_methods
};


extern "C" {

PyMODINIT_FUNC
PyInit_lang(void)
{
    PyObject *m;

    PyTypeObject *typelist[] = {
        &constant_type,
        NULL
    };

    m = PyModule_Create(&module_def);

    if (m == NULL) {
        return NULL;
    }

    for (int i=0 ; typelist[i] != NULL ; i++) {
        if (PyType_Ready(typelist[i]) < 0) {
            Py_DECREF(m);
            return NULL;
        }
        const char *name = _PyType_Name(typelist[i]);
        Py_INCREF(typelist[i]);
        PyModule_AddObject(m, name, (PyObject *)typelist[i]);
    }

    return m;
}

}
