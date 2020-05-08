"""
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

https://github.com/fpelliccioni/cpuid-py/blob/eed2a28e58edbc36c46eb14ca8f05594d1178f44/cpuid.py
"""
import struct
import typing as ta

from omnibus import lang
from omnibus import dataclasses as dc

_cpu = lang.proxy_import('._ext.cc.cpu', package=__package__)


class Cpuid(ta.NamedTuple):
    a: int
    b: int
    c: int
    d: int


def cpuid(leaf: int) -> Cpuid:
    _, a, b, c, d = _cpu.cpuid(leaf)
    return Cpuid(a, b, c, d)


def cpuid_count(leaf: int, subleaf: int) -> Cpuid:
    _, a, b, c, d = _cpu.cpuid_count(leaf, subleaf)
    return Cpuid(a, b, c, d)


def vendor() -> str:
    _, b, c, d = cpuid(0)
    return struct.pack('III', b, d, c).decode('utf-8')


def name() -> str:
    return ''.join((struct.pack('IIII', *cpuid(0x80000000 + i)).decode('utf-8') for i in range(2, 5))).strip()


def rdtscp() -> ta.Tuple[int, int]:
    return _cpu.rdtscp()


def xgetbv(ctr: int) -> int:
    return _cpu.xgetbv(ctr)


class Ident(ta.NamedTuple):
    vendor: str
    ebx: int
    edx: int
    ecx: int


# Responses identification request with %eax 0
class Idents(lang.ValueEnum):
    AMD = Ident('AuthenticAMD', 0x68747541, 0x69746e65, 0x444d4163)
    CENTAUR = Ident('CentaurHauls', 0x746e6543, 0x48727561, 0x736c7561)
    CYRIX = Ident('CyrixInstead', 0x69727943, 0x736e4978, 0x64616574)
    INTEL = Ident('GenuineIntel', 0x756e6547, 0x49656e69, 0x6c65746e)
    TM1 = Ident('TransmetaCPU', 0x6e617254, 0x74656d73, 0x55504361)
    TM2 = Ident('GenuineTMx86', 0x646f6547, 0x43534e20, 0x3638784d)
    NSC = Ident('Geode by NSC', 0x68747541, 0x69746e65, 0x79622065)
    NEXGEN = Ident('NexGenDriven', 0x4778654e, 0x72446e65, 0x6e657669)
    RISE = Ident('RiseRiseRise', 0x65736952, 0x65736952, 0x65736952)
    SIS = Ident('SiS SiS SiS ', 0x20536953, 0x20536953, 0x20536953)
    UMC = Ident('UMC UMC UMC ', 0x20434d55, 0x20434d55, 0x20434d55)
    VIA = Ident('VIA VIA VIA ', 0x20414956, 0x20414956, 0x20414956)
    VORTEX = Ident('Vortex86 SoC', 0x74726f56, 0x36387865, 0x436f5320)


class Bits(lang.Namespace):
    # Features in %ecx for leaf 1
    SSE3 = 0x00000001
    PCLMULQDQ = 0x00000002
    PCLMUL = PCLMULQDQ  # for gcc compat
    DTES64 = 0x00000004
    MONITOR = 0x00000008
    DSCPL = 0x00000010
    VMX = 0x00000020
    SMX = 0x00000040
    EIST = 0x00000080
    TM2 = 0x00000100
    SSSE3 = 0x00000200
    CNXTID = 0x00000400
    FMA = 0x00001000
    CMPXCHG16B = 0x00002000
    xTPR = 0x00004000
    PDCM = 0x00008000
    PCID = 0x00020000
    DCA = 0x00040000
    SSE41 = 0x00080000
    SSE4_1 = SSE41  # for gcc compat
    SSE42 = 0x00100000
    SSE4_2 = SSE42  # for gcc compat
    x2APIC = 0x00200000
    MOVBE = 0x00400000
    POPCNT = 0x00800000
    TSCDeadline = 0x01000000
    AESNI = 0x02000000
    AES = AESNI  # for gcc compat
    XSAVE = 0x04000000
    OSXSAVE = 0x08000000
    AVX = 0x10000000
    F16C = 0x20000000
    RDRND = 0x40000000

    # Features in %edx for leaf 1
    FPU = 0x00000001
    VME = 0x00000002
    DE = 0x00000004
    PSE = 0x00000008
    TSC = 0x00000010
    MSR = 0x00000020
    PAE = 0x00000040
    MCE = 0x00000080
    CX8 = 0x00000100
    CMPXCHG8B = CX8  # for gcc compat
    APIC = 0x00000200
    SEP = 0x00000800
    MTRR = 0x00001000
    PGE = 0x00002000
    MCA = 0x00004000
    CMOV = 0x00008000
    PAT = 0x00010000
    PSE36 = 0x00020000
    PSN = 0x00040000
    CLFSH = 0x00080000
    DS = 0x00200000
    ACPI = 0x00400000
    MMX = 0x00800000
    FXSR = 0x01000000
    FXSAVE = FXSR  # for gcc compat
    SSE = 0x02000000
    SSE2 = 0x04000000
    SS = 0x08000000
    HTT = 0x10000000
    TM = 0x20000000
    PBE = 0x80000000

    # Features in %ebx for leaf 7 sub-leaf 0
    FSGSBASE = 0x00000001
    SGX = 0x00000004
    BMI = 0x00000008
    HLE = 0x00000010
    AVX2 = 0x00000020
    SMEP = 0x00000080
    BMI2 = 0x00000100
    ENH_MOVSB = 0x00000200
    RTM = 0x00000800
    MPX = 0x00004000
    AVX512F = 0x00010000
    AVX512DQ = 0x00020000
    RDSEED = 0x00040000
    ADX = 0x00080000
    AVX512IFMA = 0x00200000
    CLFLUSHOPT = 0x00800000
    CLWB = 0x01000000
    AVX512PF = 0x04000000
    AVX51SER = 0x08000000
    AVX512CD = 0x10000000
    SHA = 0x20000000
    AVX512BW = 0x40000000
    AVX512VL = 0x80000000

    # Features in %ecx for leaf 7 sub-leaf 0
    PREFTCHWT1 = 0x00000001
    AVX512VBMI = 0x00000002
    PKU = 0x00000004
    OSPKE = 0x00000010
    AVX512VPOPCNTDQ = 0x00004000
    RDPID = 0x00400000

    # Features in %edx for leaf 7 sub-leaf 0
    AVX5124VNNIW = 0x00000004
    AVX5124FMAPS = 0x00000008

    # Features in %eax for leaf 13 sub-leaf 1
    XSAVEOPT = 0x00000001
    XSAVEC = 0x00000002
    XSAVES = 0x00000008

    # Features in %ecx for leaf 0x80000001
    LAHF_LM = 0x00000001
    ABM = 0x00000020
    SSE4a = 0x00000040
    PRFCHW = 0x00000100
    XOP = 0x00000800
    LWP = 0x00008000
    FMA4 = 0x00010000
    TBM = 0x00200000
    MWAITX = 0x20000000

    # Features in %edx for leaf 0x80000001
    MMXEXT = 0x00400000
    LM = 0x20000000
    THREEDNOWP = 0x40000000
    THREEDNOW = 0x80000000

    # Features in %ebx for leaf 0x80000001
    CLZERO = 0x00000001


class Arch(dc.Data, frozen=True, final=True):
    family: int
    model_low: ta.Optional[int]
    model_high: ta.Optional[int]
    name: str
    is_64bit: bool = False
    has_avx: bool = False


UNKNOWN_ARCH = Arch(-1, 0, 0, 'Unknown')


# https://en.wikichip.org/wiki/intel/cpuid
INTEL_ARCHS = [
    Arch(5, None, 2, 'pentium'),
    Arch(5, 4, None, 'pentiummmx'),

    Arch(6, None, 1, 'pentiumpro'),
    Arch(6, None, 6, 'pentium2'),
    Arch(6, None, 8, 'pentium3'),
    Arch(6, None, 9, 'pentiumm'),
    Arch(6, None, 0xc, 'pentium3'),
    Arch(6, None, 0xe, 'pentiumm'),
    Arch(6, None, 0x19, 'core2', True),

    Arch(6, 0x1a, 0x1a, 'nehalem', True),  # NHM Gainestown
    Arch(6, 0x1c, 0x1c, 'atom', True),  # Silverthorne
    Arch(6, 0x1d, 0x1d, 'core2', True),  # PNR Dunnington
    Arch(6, 0x1e, 0x1e, 'nehalem', True),  # NHM Lynnfield/Jasper
    Arch(6, 0x25, 0x25, 'westmere', True),  # WSM Clarkdale/Arrandale
    Arch(6, 0x26, 0x26, 'atom', True),  # Lincroft
    Arch(6, 0x27, 0x27, 'atom', True),  # Saltwell
    Arch(6, 0x2a, 0x2a, 'sandybridge', True, True),  # SB
    Arch(6, 0x2c, 0x2c, 'westmere', True),  # WSM Gulftown
    Arch(6, 0x2d, 0x2d, 'sandybridge', True, True),  # SBC-EP
    Arch(6, 0x2e, 0x2e, 'nehalem', True),  # NHM Beckton
    Arch(6, 0x2f, 0x2f, 'westmere', True),  # WSM Eagletone
    Arch(6, 0x36, 0x36, 'atom', True),  # Cedarview/Saltwell
    Arch(6, 0x37, 0x37, 'silvermont', True),  # Silvermont
    Arch(6, 0x3a, 0x3a, 'ivybridge', True, True),  # IBR
    Arch(6, 0x3c, 0x3c, 'haswell', True, True),  # Haswell client
    Arch(6, 0x3d, 0x3d, 'broadwell', True, True),  # Broadwell
    Arch(6, 0x3e, 0x3e, 'ivybridge', True, True),  # Ivytown
    Arch(6, 0x3f, 0x3f, 'haswell', True, True),  # Haswell server
    Arch(6, 0x45, 0x45, 'haswell', True, True),  # Haswell ULT
    Arch(6, 0x46, 0x46, 'haswell', True, True),  # Crystal Well
    Arch(6, 0x47, 0x47, 'broadwell', True, True),  # Broadwell
    Arch(6, 0x4a, 0x4a, 'silvermont', True),  # Silvermont
    Arch(6, 0x4c, 0x4c, 'silvermont', True),  # Airmont
    Arch(6, 0x4d, 0x4d, 'silvermont', True),  # Silvermont/Avoton
    Arch(6, 0x4e, 0x4e, 'skylake', True, True),  # Skylake client
    Arch(6, 0x4f, 0x4f, 'broadwell', True, True),  # Broadwell server
    Arch(6, 0x55, 0x55, 'skylake-avx512', True),  # Skylake server
    Arch(6, 0x56, 0x56, 'broadwell', True, True),  # Broadwell microserver
    Arch(6, 0x57, 0x57, 'knightslanding', True),  # Xeon Phi
    Arch(6, 0x5a, 0x5a, 'silvermont', True),  # Silvermont
    Arch(6, 0x5c, 0x5c, 'goldmont', True),  # Goldmont
    Arch(6, 0x5e, 0x5e, 'skylake', True, True),  # Skylake
    Arch(6, 0x5f, 0x5f, 'goldmont', True),  # Goldmont
    Arch(6, 0x8e, 0x8e, 'kabylake', True, True),  # Kabylake Y/U
    Arch(6, 0x9e, 0x9e, 'kabylake', True, True),  # Kabylake desktop

    Arch(15, None, None, 'pentium4', True),
]


AMD_ARCHS = [
    Arch(5, None, 3, 'k5'),
    Arch(5, None, 7, 'k6'),
    Arch(5, 8, 8, 'k62'),
    Arch(5, 9, 9, 'k63'),
    Arch(5, 10, 10, 'geode'),
    Arch(5, 13, 13, 'k63'),

    Arch(6, None, None, 'athlon'),

    Arch(15, None, None, 'k8', True),  # K8, K9
    Arch(16, None, None, 'k10', True),  # K10
    Arch(17, None, None, 'k8', True),  # Hybrid k8/k10, claim k8
    Arch(18, None, None, 'k10', True),  # Llano, uses K10 core
    Arch(19, None, None, 'k10', True),  # AMD Internal, assume future K10
    Arch(20, None, None, 'bobcat', True),  # Bobcat

    Arch(21, None, 1, 'bulldozer', True, True),
    Arch(21, None, 0x19, 'piledriver', True, True),  # really 2, [0x10-0x20)
    Arch(21, None, 0x3f, 'steamroller', True, True),  # really [0x30-0x40)
    Arch(21, None, None, 'excavator', True, True),  # really [0x60-0x70)

    Arch(22, None, None, 'jaguar', True, True),  # Jaguar, an improved bobcat
]


def arch() -> Arch:
    i = cpuid(1)
    family = ((i.a >> 8) & 0xf) + ((i.a >> 20) & 0xff)
    model = ((i.a >> 4) & 0xf) + ((i.a >> 12) & 0xf0)

    vendor_string = vendor()

    archs = []
    if vendor_string == 'GenuineIntel':
        archs = INTEL_ARCHS
    elif vendor_string == 'AuthenticAMD':
        archs = AMD_ARCHS
    for arch in archs:
        if (
                arch.family == family and
                (arch.model_low is None or arch.model_low >= model) and
                (arch.model_high is None or arch.model_high >= model)
        ):
            return arch

    return UNKNOWN_ARCH


def _main():
    def _is_set(leaf, reg_idx, bit):
        regs = cpuid(leaf)

        if (1 << bit) & regs[reg_idx]:
            return 'Yes'
        else:
            return '--'

    print('Vendor ID         : %s' % vendor())
    print('CPU name          : %s' % name())
    print('Arch : %s' % (arch(),))
    print('Vector instructions supported:')
    print('SSE       : %s' % _is_set(1, 3, 25))
    print('SSE2      : %s' % _is_set(1, 3, 26))
    print('SSE3      : %s' % _is_set(1, 2, 0))
    print('SSSE3     : %s' % _is_set(1, 2, 9))
    print('SSE4.1    : %s' % _is_set(1, 2, 19))
    print('SSE4.2    : %s' % _is_set(1, 2, 20))
    print('SSE4a     : %s' % _is_set(0x80000001, 2, 6))
    print('AVX       : %s' % _is_set(1, 2, 28))
    print('AVX2      : %s' % _is_set(7, 1, 5))
    print('BMI1      : %s' % _is_set(7, 1, 3))
    print('BMI2      : %s' % _is_set(7, 1, 8))


if __name__ == '__main__':
    _main()
