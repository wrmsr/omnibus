/*
MIT License

Copyright (c) 2017 Fernando Pelliccioni

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
// https://github.com/fpelliccioni/cpuid-py-native/blob/fabf0a24685ab9c87b3120ecc4c55b14613291cd/cpuid.h
#include <Python.h>

#include <stdint.h>


#if (__x86_64__ || __i386__)


#if __i386__
#define __cpuid(leaf, eax, ebx, ecx, edx) \
    __asm("cpuid" : "=a"(eax), "=b" (ebx), "=c"(ecx), "=d"(edx)
                  : "0"(leaf))

#define __cpuid_count(leaf, count, eax, ebx, ecx, edx) \
    __asm("cpuid" : "=a"(eax), "=b" (ebx), "=c"(ecx), "=d"(edx) \
                  : "0"(leaf), "2"(count))
#else // __i386__
/* x86-64 uses %rbx as the base register, so preserve it. */
#define __cpuid(leaf, eax, ebx, ecx, edx) \
    __asm("  xchgq  %%rbx,%q1\n" \
          "  cpuid\n" \
          "  xchgq  %%rbx,%q1" \
        : "=a"(eax), "=r" (ebx), "=c"(ecx), "=d"(edx) \
        : "0"(leaf))

#define __cpuid_count(leaf, count, eax, ebx, ecx, edx) \
    __asm("  xchgq  %%rbx,%q1\n" \
          "  cpuid\n" \
          "  xchgq  %%rbx,%q1" \
        : "=a"(eax), "=r" (ebx), "=c"(ecx), "=d"(edx) \
        : "0"(leaf), "2"(count))
#endif // __i386__


static __inline
int __get_cpuid_max(unsigned int leaf, unsigned int *sig) {
    unsigned int eax, ebx, ecx, edx;

#if __i386__
    int cpuid_supported;

    __asm("  pushfl\n"
          "  popl   %%eax\n"
          "  movl   %%eax,%%ecx\n"
          "  xorl   $0x00200000,%%eax\n"
          "  pushl  %%eax\n"
          "  popfl\n"
          "  pushfl\n"
          "  popl   %%eax\n"
          "  movl   $0,%0\n"
          "  cmpl   %%eax,%%ecx\n"
          "  je     1f\n"
          "  movl   $1,%0\n"
          "1:"
        : "=r" (cpuid_supported) : : "eax", "ecx");
    if (!cpuid_supported) {
        return 0;
    }
#endif // __i386__

    __cpuid(leaf, eax, ebx, ecx, edx);
    if (sig) {
        *sig = ebx;
    }
    return eax;
}


static __inline int
_cpuid(unsigned int leaf, unsigned int *eax, unsigned int *ebx, unsigned int *ecx, unsigned int *edx) {
    unsigned int max_leaf = __get_cpuid_max(leaf & 0x80000000, 0);

    if (max_leaf == 0 || max_leaf < leaf) {
        return 0;
    }

    __cpuid(leaf, *eax, *ebx, *ecx, *edx);
    return 1;
}


static __inline int
_cpuid_count(unsigned int leaf, unsigned int subleaf, unsigned int *eax, unsigned int *ebx, unsigned int *ecx, unsigned int *edx) {
    unsigned int max_leaf = __get_cpuid_max(leaf & 0x80000000, 0);

    if (max_leaf == 0 || max_leaf < leaf) {
        return 0;
    }

    __cpuid_count(leaf, subleaf, *eax, *ebx, *ecx, *edx);
    return 1;
}


//Based on https://github.com/vectorclass/version2/blob/master/instrset_detect.cpp#L21
static __inline uint64_t
_xgetbv(int ctr) {
   uint32_t a, d;
   __asm("xgetbv" : "=a"(a),"=d"(d) : "c"(ctr) : );
   return a | (uint64_t(d) << 32);
}


// https://stackoverflow.com/questions/14783782/which-inline-assembly-code-is-correct-for-rdtscp/14783846#14783846
static __inline uint64_t
_rdtscp(unsigned int *aux) {
    uint64_t rax, rdx;
    asm volatile ( "rdtscp\n" : "=a" (rax), "=d" (rdx), "=c" (aux) : : );
    return (rdx << 32) + rax;
}


#endif // (__x86_64__ || __i386__)


static PyObject *
cpuid(PyObject *self, PyObject *args) {
#if (__x86_64__ || __i386__)
    unsigned int py_leaf;

    if (!PyArg_ParseTuple(args, "I", &py_leaf)) {
        return NULL;
    }

    unsigned int eax = 0, ebx = 0, ecx = 0, edx = 0;
    int res = _cpuid(py_leaf, &eax, &ebx, &ecx, &edx);

    return Py_BuildValue("iIIII", res, eax, ebx, ecx, edx);

#else
    PyErr_SetString(PyExc_OSError, "unsupported platform");
    return NULL;

#endif
}


static PyObject *
cpuid_count(PyObject *self, PyObject *args) {
#if (__x86_64__ || __i386__)
    unsigned int py_leaf;
    unsigned int py_subleaf;

    if (!PyArg_ParseTuple(args, "II", &py_leaf, &py_subleaf)) {
        return NULL;
    }

    unsigned int eax = 0, ebx = 0, ecx = 0, edx = 0;
    int res = _cpuid_count(py_leaf, py_subleaf, &eax, &ebx, &ecx, &edx);

    return Py_BuildValue("iIIII", res, eax, ebx, ecx, edx);

#else
    PyErr_SetString(PyExc_OSError, "unsupported platform");
    return NULL;

#endif
}


static PyObject *
xgetbv(PyObject *self, PyObject *args) {
#if (__x86_64__ || __i386__)
    int py_ctr;

    if (!PyArg_ParseTuple(args, "I", &py_ctr)) {
        return NULL;
    }

    uint64_t res = _xgetbv(py_ctr);
    return Py_BuildValue("K", res);

#else
    PyErr_SetString(PyExc_OSError, "unsupported platform");
    return NULL;

#endif
}


static PyObject *
rdtscp(PyObject *self, PyObject *args) {
#if (__x86_64__ || __i386__)
    unsigned int ui = 0;
    uint64_t res = _rdtscp(&ui);

    return Py_BuildValue("(KI)", res, ui);

#else
    PyErr_SetString(PyExc_OSError, "unsupported platform");
    return NULL;

#endif
}


static PyMethodDef module_methods[] = {
    {"cpuid", cpuid, METH_VARARGS, "..."},
    {"cpuid_count", cpuid_count, METH_VARARGS, "..."},
    {"xgetbv", xgetbv, METH_VARARGS, "..."},
    {"rdtscp", rdtscp, METH_VARARGS, "..."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "cpu",
    "omnibus c++ cpu extension",
    -1,
    module_methods
};


extern "C" {

PyMODINIT_FUNC
PyInit_cpu(void)
{
    PyObject *m;

    m = PyModule_Create(&module_def);

    if (m == NULL) {
        return NULL;
    }
    return m;
}

}
