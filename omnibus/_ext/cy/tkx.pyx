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


cdef Tcl_CreateCommand_t TCL_CREATE_COMMAND = NULL
cdef Tcl_AppendResult_t TCL_APPEND_RESULT = NULL
cdef Tk_FindPhoto_t TK_FIND_PHOTO = NULL
cdef Tk_PhotoPutBlock_85_t TK_PHOTO_PUT_BLOCK_85 = NULL


DEF PHOTO_MODE_BW = 0
DEF PHOTO_MODE_RGB = 1
DEF PHOTO_MODE_RGBA = 2

cdef struct PhotoData:
    int mode
    int xsize
    int ysize
    int pixelsize
    char *pixels


cdef int PhotoPut(ClientData clientdata, Tcl_Interp* interp, int argc, const char **argv):
    if argc != 3:
        TCL_APPEND_RESULT(interp, b'usage: ', argv[0], b' destPhoto srcImage', <char*> NULL)
        return TCL_ERROR

    photo = TK_FIND_PHOTO(interp, argv[1])
    if photo == NULL:
        TCL_APPEND_RESULT(interp, b'destination photo must exist', <char*> NULL)
        return TCL_ERROR

    cdef PhotoData* pd = <PhotoData*><ssize_t>int(argv[2])
    if pd.pixels == NULL:
        TCL_APPEND_RESULT(interp, b'bad display memory', <char*> NULL)
        return TCL_ERROR

    cdef Tk_PhotoImageBlock block

    if pd.mode == PHOTO_MODE_BW:
        block.pixelSize = 1
        block.offset[0] = block.offset[1] = block.offset[2] = block.offset[3] = 0
    elif pd.mode[:3] in (PHOTO_MODE_RGB, PHOTO_MODE_RGBA):
        block.pixelSize = 4
        block.offset[0] = 0
        block.offset[1] = 1
        block.offset[2] = 2
        if pd.mode == PHOTO_MODE_RGBA:
            block.offset[3] = 3
        else:
            block.offset[3] = 0
    else:
        TCL_APPEND_RESULT(interp, b'Bad mode', <char*> NULL)
        return TCL_ERROR

    block.width = pd.xsize
    block.height = pd.ysize
    block.pitch = pd.xsize * pd.pixelsize
    block.pixelPtr = <unsigned char*> pd.pixels

    TK_PHOTO_PUT_BLOCK_85(interp, photo, &block, 0, 0, block.width, block.height, TK_PHOTO_COMPOSITE_SET)

    return TCL_OK


def init(size_t interp):
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

    TCL_CREATE_COMMAND(<Tcl_Interp*>interp, 'omnibus_tkx_photo', <Tcl_CmdProc*>PhotoPut, <ClientData> 0, <Tcl_CmdDeleteProc*> NULL)
