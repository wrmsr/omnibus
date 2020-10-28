DEF TCL_OK = 0
DEF TCL_ERROR = 1

ctypedef void Tcl_Interp;
ctypedef void *Tcl_Command;
ctypedef void *ClientData;

ctypedef int (*Tcl_CmdProc) (ClientData clientData, Tcl_Interp *interp, int argc, const char *argv[]);
ctypedef void (*Tcl_CmdDeleteProc) (ClientData clientData);

ctypedef Tcl_Command (*Tcl_CreateCommand_t)(Tcl_Interp *interp, const char *cmdName, Tcl_CmdProc *proc, ClientData clientData, Tcl_CmdDeleteProc *deleteProc);
ctypedef void (*Tcl_AppendResult_t) (Tcl_Interp *interp, ...);

DEF TK_PHOTO_COMPOSITE_OVERLAY = 0
DEF TK_PHOTO_COMPOSITE_SET = 1

ctypedef void *Tk_PhotoHandle

cdef struct Tk_PhotoImageBlock:
    unsigned char *pixelPtr
    int width
    int height
    int pitch
    int pixel_size
    int offset[4]

ctypedef int (*Tk_PhotoPutBlock_85_t) (Tcl_Interp * interp, Tk_PhotoHandle handle, Tk_PhotoImageBlock * blockPtr, int x, int y, int width, int height, int compRule)  # noqa
ctypedef Tk_PhotoHandle (*Tk_FindPhoto_t) (Tcl_Interp *interp, const char *imageName)  # noqa


cdef Tcl_CreateCommand_t TCL_CREATE_COMMAND
cdef Tcl_AppendResult_t TCL_APPEND_RESULT
cdef Tk_FindPhoto_t TK_FIND_PHOTO
cdef Tk_PhotoPutBlock_85_t TK_PHOTO_PUT_BLOCK_85


def init():
    import ctypes as ct
    mod = ct.CDLL(None)
    if not hasattr(mod, 'Tcl_CreateCommand'):
        import tkinter
        mod = ct.CDLL(tkinter._tkinter.__file__)

    global TCL_CREATE_COMMAND
    TCL_CREATE_COMMAND = (<Tcl_CreateCommand_t*><size_t>ct.addressof(mod.Tcl_CreateCommand))[0]
    global TCL_APPEND_RESULT
    TCL_APPEND_RESULT = (<Tcl_AppendResult_t*><size_t>ct.addressof(mod.Tcl_AppendResult))[0]
    global TK_FIND_PHOTO
    TK_FIND_PHOTO = (<Tk_FindPhoto_t*><size_t>ct.addressof(mod.Tk_FindPhoto))[0]
    global TK_PHOTO_PUT_BLOCK_85
    TK_PHOTO_PUT_BLOCK_85 = (<Tk_PhotoPutBlock_85_t*><size_t>ct.addressof(mod.Tk_PhotoPutBlock))[0]
