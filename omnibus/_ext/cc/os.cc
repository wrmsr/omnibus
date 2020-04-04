#include <unistd.h>

#if __linux__
#include <sys/syscall.h>

#elif __APPLE__
#include <pthread.h>

#endif

#include <Python.h>


static PyObject *
gettid(PyObject *self, PyObject *args)
{
#if __linux__
    uint64_t tid = syscall(SYS_gettid);
    return Py_BuildValue("k", tid);

#elif __APPLE__
    uint64_t tid;
    pthread_threadid_np(NULL, &tid);
    return Py_BuildValue("k", tid);

#else
    PyErr_SetString(PyExc_OSError, "unsupported platform");
    return NULL;

#endif
}


static PyMethodDef module_methods[] = {
    {"gettid", gettid, METH_NOARGS, "get thread id"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "os",
    "omnibus c++ os extension",
    -1,
    module_methods
};


extern "C" {

PyMODINIT_FUNC
PyInit_os(void)
{
    PyObject *m;

    m = PyModule_Create(&module_def);

    if (m == NULL) {
        return NULL;
    }
    return m;
}

}
