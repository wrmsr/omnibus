#include <Python.h>

#include <unistd.h>

#if __linux__
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/syscall.h>

#elif __APPLE__
#include <ifaddrs.h>
#include <net/if_dl.h>
#include <net/if_types.h>
#include <net/route.h>
#include <pthread.h>

#endif


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


static PyObject *
getmac(PyObject *self, PyObject *args)
{
    char *name = NULL;
    int hwlen = 6;

    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

#if __linux__
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        Py_RETURN_NONE;
    }

    struct ifreq ifr = {0};
    strncpy(ifr.ifr_name, name, IFNAMSIZ - 1);

    if (ioctl(sock, SIOCGIFHWADDR, &ifr)) {
        close(sock);
        Py_RETURN_NONE;
    }

    close(sock);
    return PyBytes_FromStringAndSize(ifr.ifr_hwaddr.sa_data, hwlen);

#elif __APPLE__
    struct ifaddrs *addrs = NULL;
    if (getifaddrs(&addrs) != -1) {
        for (struct ifaddrs *ifa = addrs; ifa; ifa = ifa->ifa_next) {
            if (ifa->ifa_addr->sa_family == AF_LINK && !strcmp(ifa->ifa_name, name)) {
                struct sockaddr_dl* sdl = (struct sockaddr_dl*)ifa->ifa_addr;
                if (sdl->sdl_type == IFT_ETHER) {
                    return PyBytes_FromStringAndSize(LLADDR(sdl), hwlen);
                }
            }
        }
        freeifaddrs(addrs);
    }
    Py_RETURN_NONE;

#else
    PyErr_SetString(PyExc_OSError, "unsupported platform");
    return NULL;

#endif
}


static PyMethodDef module_methods[] = {
    {"gettid", gettid, METH_NOARGS, "get thread id"},
    {"getmac", getmac, METH_VARARGS, "get mac"},
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
