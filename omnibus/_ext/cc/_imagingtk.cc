#include "Python.h"

#include <dlfcn.h>
#include <stdint.h>
#include <stdlib.h>


typedef uint8_t UINT8;
typedef int32_t INT32;

typedef struct ImagingMemoryInstance* Imaging;

typedef struct ImagingPaletteInstance* ImagingPalette;

#define IMAGING_TYPE_UINT8 0
#define IMAGING_TYPE_INT32 1
#define IMAGING_TYPE_FLOAT32 2
#define IMAGING_TYPE_SPECIAL 3

#define IMAGING_MODE_LENGTH 6+1 /* Band names ("1", "L", "P", "RGB", "RGBA", "CMYK", "YCbCr", "BGR;xy") */

typedef struct {
    char *ptr;
    int size;
} ImagingMemoryBlock;

struct ImagingMemoryInstance {
    char mode[IMAGING_MODE_LENGTH];
    int type;           /* Data type (IMAGING_TYPE_*) */
    int depth;          /* Depth (ignored in this version) */
    int bands;          /* Number of bands (1, 2, 3, or 4) */
    int xsize;          /* Image dimension. */
    int ysize;

    ImagingPalette palette;

    UINT8 **image8;     /* Set for 8-bit images (pixelsize=1). */
    INT32 **image32;    /* Set for 32-bit images (pixelsize=4). */

    char **image;       /* Actual raster data. */
    char *block;        /* Set if data is allocated in a single block. */
    ImagingMemoryBlock *blocks;     /* Memory blocks for pixel storage */

    int pixelsize;      /* Size of a pixel, in bytes (1, 2 or 4) */
    int linesize;       /* Size of a line, in bytes (xsize * pixelsize) */

    void (*destroy)(Imaging im);
};

#define IMAGING_PIXEL_1(im,x,y) ((im)->image8[(y)][(x)])
#define IMAGING_PIXEL_L(im,x,y) ((im)->image8[(y)][(x)])
#define IMAGING_PIXEL_LA(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_P(im,x,y) ((im)->image8[(y)][(x)])
#define IMAGING_PIXEL_PA(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_I(im,x,y) ((im)->image32[(y)][(x)])
#define IMAGING_PIXEL_F(im,x,y) (((FLOAT32*)(im)->image32[y])[x])
#define IMAGING_PIXEL_RGB(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_RGBA(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_CMYK(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_YCbCr(im,x,y) ((im)->image[(y)][(x)*4])

#define IMAGING_PIXEL_UINT8(im,x,y) ((im)->image8[(y)][(x)])
#define IMAGING_PIXEL_INT32(im,x,y) ((im)->image32[(y)][(x)])
#define IMAGING_PIXEL_FLOAT32(im,x,y) (((FLOAT32*)(im)->image32[y])[x])


#define TCL_OK 0
#define TCL_ERROR 1

typedef struct Tcl_Interp Tcl_Interp;

typedef struct Tcl_Command_ *Tcl_Command;
typedef void *ClientData;

typedef int (Tcl_CmdProc) (ClientData clientData, Tcl_Interp *interp, int argc, const char *argv[]);
typedef void (Tcl_CmdDeleteProc) (ClientData clientData);

typedef Tcl_Command (*Tcl_CreateCommand_t)(Tcl_Interp *interp, const char *cmdName, Tcl_CmdProc *proc, ClientData clientData, Tcl_CmdDeleteProc *deleteProc);
typedef void (*Tcl_AppendResult_t) (Tcl_Interp *interp, ...);

#define TK_PHOTO_COMPOSITE_OVERLAY 0
#define TK_PHOTO_COMPOSITE_SET 1

typedef void *Tk_PhotoHandle;

typedef struct Tk_PhotoImageBlock
{
    unsigned char *pixelPtr;
    int width;
    int height;
    int pitch;
    int pixelSize;
    int offset[4];
} Tk_PhotoImageBlock;

typedef int (*Tk_PhotoPutBlock_85_t) (Tcl_Interp * interp, Tk_PhotoHandle handle, Tk_PhotoImageBlock * blockPtr, int x, int y, int width, int height, int compRule);
typedef Tk_PhotoHandle (*Tk_FindPhoto_t) (Tcl_Interp *interp, const char *imageName);


static Tcl_CreateCommand_t TCL_CREATE_COMMAND;
static Tcl_AppendResult_t TCL_APPEND_RESULT;
static Tk_FindPhoto_t TK_FIND_PHOTO;
static Tk_PhotoPutBlock_85_t TK_PHOTO_PUT_BLOCK_85;

static Imaging
ImagingFind(const char* name)
{
    Py_ssize_t id;
    id = atol(name);
    if (!id) {
        return NULL;
    }
    return (Imaging) id;
}

static int
PyImagingPhotoPut(ClientData clientdata, Tcl_Interp* interp, int argc, const char **argv)
{
    Imaging im;
    Tk_PhotoHandle photo;
    Tk_PhotoImageBlock block;

    if (argc != 3) {
        TCL_APPEND_RESULT(interp, "usage: ", argv[0], " destPhoto srcImage", (char *) NULL);
        return TCL_ERROR;
    }

    photo = TK_FIND_PHOTO(interp, argv[1]);
    if (photo == NULL) {
        TCL_APPEND_RESULT( interp, "destination photo must exist", (char *) NULL );
        return TCL_ERROR;
    }

    im = ImagingFind(argv[2]);
    if (!im) {
        TCL_APPEND_RESULT(interp, "bad name", (char*) NULL);
        return TCL_ERROR;
    }
    if (!im->block) {
        TCL_APPEND_RESULT(interp, "bad display memory", (char*) NULL);
        return TCL_ERROR;
    }

    if (strcmp(im->mode, "1") == 0 || strcmp(im->mode, "L") == 0) {
        block.pixelSize = 1;
        block.offset[0] = block.offset[1] = block.offset[2] = block.offset[3] = 0;
    } else if (strncmp(im->mode, "RGB", 3) == 0) {
        block.pixelSize = 4;
        block.offset[0] = 0;
        block.offset[1] = 1;
        block.offset[2] = 2;
        if (strcmp(im->mode, "RGBA") == 0) {
            block.offset[3] = 3; /* alpha (or reserved, under 8.2) */
        } else {
            block.offset[3] = 0; /* no alpha */
        }
    } else {
        TCL_APPEND_RESULT(interp, "Bad mode", (char*) NULL);
        return TCL_ERROR;
    }

    block.width = im->xsize;
    block.height = im->ysize;
    block.pitch = im->linesize;
    block.pixelPtr = (unsigned char*) im->block;

    TK_PHOTO_PUT_BLOCK_85(interp, photo, &block, 0, 0, block.width, block.height, TK_PHOTO_COMPOSITE_SET);

    return TCL_OK;
}

void
TkImaging_Init(Tcl_Interp* interp)
{
    TCL_CREATE_COMMAND(interp, "PyImagingPhoto", PyImagingPhotoPut, (ClientData) 0, (Tcl_CmdDeleteProc*) NULL);
}


char *fname2char(PyObject *fname)
{
    PyObject* bytes;
    bytes = PyUnicode_EncodeFSDefault(fname);
    if (bytes == NULL) {
        return NULL;
    }
    return PyBytes_AsString(bytes);
}

void *_dfunc(void *lib_handle, const char *func_name)
{
    void* func;
    dlerror();
    func = dlsym(lib_handle, func_name);
    if (func == NULL) {
        const char *error = dlerror();
        PyErr_SetString(PyExc_RuntimeError, error);
    }
    return func;
}

int _func_loader(void *lib)
{
    if ((TCL_CREATE_COMMAND = (Tcl_CreateCommand_t) _dfunc(lib, "Tcl_CreateCommand")) == NULL) { return 1; }
    if ((TCL_APPEND_RESULT = (Tcl_AppendResult_t) _dfunc(lib, "Tcl_AppendResult")) == NULL) { return 1; }
    if ((TK_FIND_PHOTO = (Tk_FindPhoto_t) _dfunc(lib, "Tk_FindPhoto")) == NULL) { return 1; }
    return ((TK_PHOTO_PUT_BLOCK_85 = (Tk_PhotoPutBlock_85_t) _dfunc(lib, "Tk_PhotoPutBlock")) == NULL);
}

int load_tkinter_funcs(void)
{
    int ret = -1;
    void *main_program, *tkinter_lib;
    char *tkinter_libname;
    PyObject *pModule = NULL, *pString = NULL;

    main_program = dlopen(NULL, RTLD_LAZY);
    if (_func_loader(main_program) == 0) {
        dlclose(main_program);
        return 0;
    }
    PyErr_Clear();

    pModule = PyImport_ImportModule("tkinter._tkinter");
    if (pModule == NULL) {
        goto exit;
    }
    pString = PyObject_GetAttrString(pModule, "__file__");
    if (pString == NULL) {
        goto exit;
    }
    tkinter_libname = fname2char(pString);
    if (tkinter_libname == NULL) {
        goto exit;
    }
    tkinter_lib = dlopen(tkinter_libname, RTLD_LAZY);
    if (tkinter_lib == NULL) {
        PyErr_SetString(PyExc_RuntimeError,
                "Cannot dlopen tkinter module file");
        goto exit;
    }
    ret = _func_loader(tkinter_lib);
    dlclose(tkinter_lib);
exit:
    dlclose(main_program);
    Py_XDECREF(pModule);
    Py_XDECREF(pString);
    return ret;
}


typedef struct {
    PyObject_HEAD
    Tcl_Interp* interp;
} TkappObject;

static PyObject*
_tkinit(PyObject* self, PyObject* args)
{
    Tcl_Interp* interp;

    PyObject* arg;
    int is_interp;
    if (!PyArg_ParseTuple(args, "Oi", &arg, &is_interp)) {
        return NULL;
    }

    if (is_interp) {
        interp = (Tcl_Interp*)PyLong_AsVoidPtr(arg);
    } else {
        TkappObject* app;
        app = (TkappObject*)PyLong_AsVoidPtr(arg);
        interp = app->interp;
    }

    TkImaging_Init(interp);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef functions[] = {
    {"tkinit", (PyCFunction)_tkinit, 1},
    {NULL, NULL}
};

PyMODINIT_FUNC
PyInit__imagingtk(void) {
    static PyModuleDef module_def = {
        PyModuleDef_HEAD_INIT,
        "_imagingtk",       /* m_name */
        NULL,               /* m_doc */
        -1,                 /* m_size */
        functions,          /* m_methods */
    };
    PyObject *m;
    m = PyModule_Create(&module_def);
    return (load_tkinter_funcs() == 0) ? m : NULL;
}
