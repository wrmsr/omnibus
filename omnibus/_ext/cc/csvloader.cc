/*
Copyright (c) 2016 Jeroen van der Heijden / Transceptor Technology

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

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
// CSV Loader module
// 2016, Jeroen van der Heijden (Transceptor Technology)
#include <Python.h>
#include <stdbool.h>
#include <math.h>
#include <stddef.h>

#define INIT_ALLOC_SZ 64


// FIXME: no globals.
static char *quoted_str = NULL;
static Py_ssize_t quoted_len = 0;


static char *
replace_str(const char *content, Py_ssize_t *length)
{
    *length -= 2;
    if (quoted_len < *length) {
        char *tmp = (char *) realloc(quoted_str, *length);
        if (tmp == NULL) {
            PyErr_SetString(PyExc_MemoryError, "Memory re-allocation error.");
            return NULL;
        }
        quoted_str = tmp;
    }

    content++;
    char *dp = quoted_str;

    for (Py_ssize_t i = *length; i--; content++, dp++) {
        if (*content == '"') {
            i--;
            content++;
            (*length)--;
        }
        *dp = *content;
    }

    return quoted_str;
}


static int
loads(PyObject *grid, Py_ssize_t length, const char *content)
{
    PyObject *row;
    if ((row = PyList_New(0)) == NULL) {
        return -1;
    }

    int rc;
    bool in_quotes = false;
    bool is_quoted = false;
    bool is_int = true;
    bool is_float = true;
    Py_ssize_t word_len = 0;
    Py_ssize_t replace_len;
    PyObject *obj;

    // Loop through the content using the length
    while (length--) {
        char c = content[word_len];

        // Check if we have an not-quoted comma or end-of-line character.
        if (!in_quotes && (c == ',' || c == '\n')) {
            // Set the correct object type
            if (!word_len) {
                obj = Py_None;
                Py_INCREF(obj);
            }
            else if (is_int) {
                obj = PyLong_FromSsize_t((Py_ssize_t) strtoll(content, NULL, 0));
            }
            else if (is_float) {
                obj = PyFloat_FromDouble(strtod(content, NULL));
            }
            else if (is_quoted) {
                replace_len = word_len;
                if (replace_str(content, &replace_len) == NULL) {
                    Py_DECREF(row);
                    return -1;
                }
                obj = PyUnicode_FromStringAndSize(quoted_str, replace_len);
            }
            else {
                obj = PyUnicode_FromStringAndSize(content, word_len);
            }

            if (obj == NULL) {
                Py_DECREF(row);
                return -1;
            }

            // Append value to the row.
            rc = PyList_Append(row, obj);
            Py_DECREF(obj);

            if (rc == -1) {
                Py_DECREF(row);
                return -1;
            }

            // Update variables.
            content += word_len + 1;
            word_len = 0;
            is_quoted = false;
            is_int = true;
            is_float = true;

            // Do some stuff when we have an end-of-line detected.
            if (c == '\n') {
                rc = PyList_Append(grid, row);
                Py_DECREF(row);

                row = PyList_New(0);
                if (rc == -1 || row == NULL) {
                    Py_DECREF(grid);
                    return -1;
                }
            }

            continue;
        }

        if (c == '"') {
            if (!word_len) {
                is_quoted = true;
            }
            if (is_quoted) {
                in_quotes = !in_quotes;
            }
        }
        else if (is_quoted && !in_quotes) {
            Py_DECREF(row);
            PyErr_SetString(PyExc_ValueError, "Wrong string escaping found");
            return -1;
        }

        if (is_float && !isdigit(c) && (word_len != 0 || c != '-')) {
            if (is_float && c == '.') {
                if (is_int) {
                    is_int = false;
                }
                else {
                    is_float = false;
                }
            }
            else {
                is_int = false;
                is_float = false;
            }
        }
        word_len++;
    }
    if (in_quotes) {
        Py_DECREF(row);
        PyErr_SetString(PyExc_ValueError, "Wrong string escaping found");
        return -1;
    }

    // Set the correct object type
    if (!word_len) {
        obj = Py_None;
        Py_INCREF(obj);
    }
    else if (is_int) {
        obj = PyLong_FromSsize_t((Py_ssize_t) strtoll(content, NULL, 0));
    }
    else if (is_float) {
        obj = PyFloat_FromDouble(strtod(content, NULL));
    }
    else if (is_quoted) {
        replace_len = word_len;
        if (replace_str(content, &replace_len) == NULL) {
            Py_DECREF(row);
            return -1;
        }
        obj = PyUnicode_FromStringAndSize(quoted_str, replace_len);
    }
    else {
        obj = PyUnicode_FromStringAndSize(content, word_len);
    }

    if (obj == NULL) {
        Py_DECREF(row);
        return -1;
    }

    // Append the last value to the row.
    rc = PyList_Append(row, obj);
    Py_DECREF(obj);

    if (rc == 0) {
        // Append the last row to the grid.
        rc = PyList_Append(grid, row);
        Py_DECREF(row);
    }

    return rc;
}


static PyObject *
csvloader_loads(PyObject *self, PyObject *args)
{
    int arg_size = PyTuple_GET_SIZE(args);
    if (arg_size != 1) {
        PyErr_SetString(PyExc_TypeError, "loads() missing 1 required positional argument");
        return NULL;
    }

    // Check for a valid string and set content and length variable
    PyObject *obj = PyTuple_GET_ITEM(args, 0);

    if (!PyUnicode_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "loads() first argument must be a string.");
        return NULL;
    }

    const char *content = NULL;
    Py_ssize_t length;
    if ((content = PyUnicode_AsUTF8AndSize(obj, &length)) == NULL) {
        return NULL;
    }

    // Create grid
    if ((obj = PyList_New(0)) == NULL) {
        return NULL;
    }

    // Warning: we use a static quoted_str so we do not need to allocate space for each quoted string. This is however
    // not thread safe and should be solved different in case we need to be.
    quoted_len = INIT_ALLOC_SZ;
    quoted_str = (char *) malloc(quoted_len);

    if (quoted_str == NULL || loads(obj, length, content)) {
        if (quoted_str == NULL) {
            PyErr_SetString(PyExc_MemoryError, "Memory allocation error");
        }
        Py_DECREF(obj);
        obj = NULL;
    }

    free(quoted_str);

    return obj;
}


static const char *loads_docstring =
    "Returns a 2 dimensional array for the given CSV content.\n"
    "\n"
    "Each field in the CSV will be type casted to either a integer, float,\n"
    "string or None value. An empty field will be casted to None, except when\n"
    "the field explicit has an empty string defined by two. In that case we\n"
    "will return an empty string instead of None.";


static PyMethodDef module_methods[] =
{
    {"loads", (PyCFunction)csvloader_loads, METH_VARARGS, loads_docstring},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "csvloader",
    "omnibus csvloader",
    -1,
    module_methods
};


extern "C" {

PyMODINIT_FUNC
PyInit_csvloader(void)
{
    PyObject *m;

    m = PyModule_Create(&module_def);

    if (m == NULL) {
        return NULL;
    }
    return m;
}

}
