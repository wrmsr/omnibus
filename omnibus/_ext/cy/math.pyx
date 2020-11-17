cdef extern from "math.h":
    float       fmaf(float x, float y, float z)
    double      fma(double x, double y, double z)
    long double fmal(long double x, long double y, long double z)


def fmaf_(float x, float y, float z):
    return fmaf(x, y, z)


def fma_(double x, double y, double z):
    return fma(x, y, z)


def fmal_(long double x, long double y, long double z):
    return fmal(x, y, z)
