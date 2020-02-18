import ctypes as ct

from .. import ctypes as bct
from .. import lang


def test_cstruct():
    class C(bct.AutoStructure):
        def f(self, x: ct.c_int) -> None: pass
        g = ct.c_int


def test_jni():
    jint = ct.c_int

    class JNIEnv(ct.Structure):
        pass

    JNIEnv_p = ct.POINTER(JNIEnv)

    class NativeInterface(bct.AutoStructure):
        locals().update({f'reserved{i}': ct.c_void_p for i in range(4)})

        def GetVersion(self, env: JNIEnv_p) -> jint: lang.void()

    jni = ct.cast(0, ct.POINTER(NativeInterface))  # noqa
