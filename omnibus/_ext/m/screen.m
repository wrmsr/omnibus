/*
-framework AppKit
-framework CoreFoundation
*/
#include <unistd.h>

#if __APPLE__
#include <AppKit/NSScreen.h>

#endif

#include <Python.h>


static PyObject *
backing_scale_factor(PyObject *self, PyObject *args)
{
#if __APPLE__
    float value = [[NSScreen mainScreen] backingScaleFactor];
    return Py_BuildValue("f", value);

#else
    PyErr_SetString(PyExc_OSError, "unsupported platform");
    return NULL;

#endif
}


static PyMethodDef module_methods[] = {
    {"backing_scale_factor", backing_scale_factor, METH_NOARGS, "get backing scale factor"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "screen",
    "omnibus obj-c screen extension",
    -1,
    module_methods
};


PyMODINIT_FUNC
PyInit_screen(void)
{
    PyObject *m;

    m = PyModule_Create(&module_def);

    if (m == NULL) {
        return NULL;
    }
    return m;
}
