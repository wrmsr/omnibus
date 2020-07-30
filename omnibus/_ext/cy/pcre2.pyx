"""
MIT License

Copyright (c) 2017 Gu Pengfei

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
"""
from cpython.mem cimport PyMem_Free
from cpython.mem cimport PyMem_Malloc
from libc.stdint cimport uint32_t
from libc.stdint cimport uint8_t
from libc.string cimport memcpy


cdef extern from "_pcre2.h":
    enum:
        PCRE2_ZERO_TERMINATED
        PCRE2_ERROR_NOMATCH

        # jit
        PCRE2_JIT_COMPLETE
        PCRE2_JIT_PARTIAL_SOFT
        PCRE2_JIT_PARTIAL_HARD

        # compile options
        PCRE2_ALLOW_EMPTY_CLASS
        PCRE2_ALT_BSUX
        PCRE2_AUTO_CALLOUT
        PCRE2_CASELESS
        PCRE2_DOLLAR_ENDONLY
        PCRE2_DOTALL
        PCRE2_DUPNAMES
        PCRE2_EXTENDED
        PCRE2_FIRSTLINE
        PCRE2_MATCH_UNSET_BACKREF
        PCRE2_MULTILINE
        PCRE2_NEVER_UCP
        PCRE2_NEVER_UTF
        PCRE2_NO_AUTO_CAPTURE
        PCRE2_NO_AUTO_POSSESS
        PCRE2_NO_DOTSTAR_ANCHOR
        PCRE2_NO_START_OPTIMIZE
        PCRE2_UCP
        PCRE2_UNGREEDY
        PCRE2_UTF
        PCRE2_NEVER_BACKSLASH_C
        PCRE2_ALT_CIRCUMFLEX
        PCRE2_ALT_VERBNAMES
        PCRE2_USE_OFFSET_LIMIT

    cdef struct pcre2_real_general_context:
        pass
    ctypedef pcre2_real_general_context pcre2_general_context

    cdef struct pcre2_real_compile_context:
        pass
    ctypedef pcre2_real_compile_context pcre2_compile_context

    cdef struct pcre2_real_match_context:
        pass
    ctypedef pcre2_real_match_context pcre2_match_context

    cdef struct pcre2_real_code:
        pass
    ctypedef pcre2_real_code pcre2_code

    cdef struct pcre2_real_match_data:
        pass
    ctypedef pcre2_real_match_data pcre2_match_data

    ctypedef const uint8_t *PCRE2_SPTR
    ctypedef size_t PCRE2_SIZE

    # compile and match
    pcre2_code *pcre2_compile(
            PCRE2_SPTR,
            PCRE2_SIZE,
            uint32_t,
            int *,
            PCRE2_SIZE *,
            pcre2_compile_context *,
    )
    int pcre2_match(
            const pcre2_code *,
            PCRE2_SPTR,
            PCRE2_SIZE,
            PCRE2_SIZE,
            uint32_t,
            pcre2_match_data *,
            pcre2_match_context *,
    )
    # Alternative algorithm (said DFA but rather TNFA)
    int pcre2_dfa_match(
            const pcre2_code *,
            PCRE2_SPTR,
            PCRE2_SIZE,
            PCRE2_SIZE,
            uint32_t,
            pcre2_match_data *,
            pcre2_match_context *,
            int*,
            PCRE2_SIZE,
    )
    # jit
    int pcre2_jit_compile(pcre2_code *, uint32_t)
    int pcre2_jit_match(
            const pcre2_code *,
            PCRE2_SPTR,
            PCRE2_SIZE,
            PCRE2_SIZE,
            uint32_t,
            pcre2_match_data *,
            pcre2_match_context *,
    )

    # match data
    pcre2_match_data *pcre2_match_data_create_from_pattern(const pcre2_code *, pcre2_general_context *)
    void pcre2_match_data_free(pcre2_match_data *)

    # re code
    void pcre2_code_free(pcre2_code *)

    PCRE2_SIZE *pcre2_get_ovector_pointer(pcre2_match_data *)


ctypedef int(*match_func_type)(
        const pcre2_code *,
        PCRE2_SPTR,
        PCRE2_SIZE,
        PCRE2_SIZE,
        uint32_t,
        pcre2_match_data *,
        pcre2_match_context *,
)

ctypedef int(*dfa_match_func_type)(
        const pcre2_code *,
        PCRE2_SPTR,
        PCRE2_SIZE,
        PCRE2_SIZE,
        uint32_t,
        pcre2_match_data *,
        pcre2_match_context *,
        int *,
        PCRE2_SIZE,
)


# jit
JIT_COMPLETE = PCRE2_JIT_COMPLETE
JIT_PARTIAL_SOFT = PCRE2_JIT_PARTIAL_SOFT
JIT_PARTIAL_HARD = PCRE2_JIT_PARTIAL_HARD

# compile options
ALLOW_EMPTY_CLASS = PCRE2_ALLOW_EMPTY_CLASS
ALT_BSUX = PCRE2_ALT_BSUX
AUTO_CALLOUT = PCRE2_AUTO_CALLOUT
CASELESS = PCRE2_CASELESS
DOLLAR_ENDONLY = PCRE2_DOLLAR_ENDONLY
DOTALL = PCRE2_DOTALL
DUPNAMES = PCRE2_DUPNAMES
EXTENDED = PCRE2_EXTENDED
FIRSTLINE = PCRE2_FIRSTLINE
MATCH_UNSET_BACKREF = PCRE2_MATCH_UNSET_BACKREF
MULTILINE = PCRE2_MULTILINE
NEVER_UCP = PCRE2_NEVER_UCP
NEVER_UTF = PCRE2_NEVER_UTF
NO_AUTO_CAPTURE = PCRE2_NO_AUTO_CAPTURE
NO_AUTO_POSSESS = PCRE2_NO_AUTO_POSSESS
NO_DOTSTAR_ANCHOR = PCRE2_NO_DOTSTAR_ANCHOR
NO_START_OPTIMIZE = PCRE2_NO_START_OPTIMIZE
UCP = PCRE2_UCP
UNGREEDY = PCRE2_UNGREEDY
UTF = PCRE2_UTF
NEVER_BACKSLASH_C = PCRE2_NEVER_BACKSLASH_C
ALT_CIRCUMFLEX = PCRE2_ALT_CIRCUMFLEX
ALT_VERBNAMES = PCRE2_ALT_VERBNAMES
USE_OFFSET_LIMIT = PCRE2_USE_OFFSET_LIMIT


cdef class PCRE2:
    cdef bint use_alternative_algorithm
    cdef unsigned char *_pattern
    cdef int *_workspace
    cdef PCRE2_SIZE _workspace_len
    cdef int error_number
    cdef PCRE2_SIZE error_offset
    cdef pcre2_code*re_code
    cdef pcre2_match_data*match_data
    cdef match_func_type match_func
    cdef dfa_match_func_type dfa_match_func

    def __cinit__(
            self,
            bytes pattern,
            uint32_t options = 0,
            uint32_t jit_option = PCRE2_JIT_COMPLETE,
            bint use_alternative_algorithm = False,
    ):
        cdef size_t length = len(pattern)
        self._pattern = <unsigned char *> PyMem_Malloc((length + 1) * sizeof(unsigned char))
        if not self._pattern:
            raise MemoryError
        self.use_alternative_algorithm = use_alternative_algorithm

        memcpy(self._pattern, <unsigned char *> pattern, length)
        self._pattern[length] = b'\0'

        self.re_code = pcre2_compile(
            <PCRE2_SPTR> self._pattern,
            PCRE2_ZERO_TERMINATED,
            options,
            &self.error_number,
            &self.error_offset,
            NULL
        )
        if not self.re_code:
            raise ValueError(f'Failed to compile pattern at offset: {self.error_offset}.')

        if not use_alternative_algorithm:
            if pcre2_jit_compile(self.re_code, jit_option) == 0:
                self.match_func = pcre2_jit_match
            else:
                self.match_func = pcre2_match
        else:
            self.dfa_match_func = pcre2_dfa_match
            self._workspace_len = 1000
            self._workspace = <int*> PyMem_Malloc(self._workspace_len * sizeof(int))
            if not self._workspace:
                raise MemoryError
        self.match_data = pcre2_match_data_create_from_pattern(self.re_code, NULL)

    def search(self, bytes content, int offset=0):
        cdef int match_count

        if self.use_alternative_algorithm:
            match_count = self.dfa_match_func(
                self.re_code,
                <PCRE2_SPTR> content,
                len(content),
                offset,
                0,
                self.match_data,
                NULL,
                <int*> self._workspace,
                self._workspace_len,
            )
        else:
            match_count = self.match_func(
                self.re_code,
                <PCRE2_SPTR> content,
                len(content),
                offset,
                0,
                self.match_data,
                NULL,
            )
        if match_count < 0:
            if match_count == PCRE2_ERROR_NOMATCH:
                return None
            else:
                return None

        if match_count == 0:
            raise MemoryError("ovector was not big enough for all the captured substrings")

        return ResultFactory(content, match_count, self.match_data, self.use_alternative_algorithm)

    def __dealloc__(self):
        if self._pattern:
            PyMem_Free(self._pattern)
            self._pattern = NULL
        if self.match_data:
            pcre2_match_data_free(self.match_data)
            self.match_data = NULL
        if self.re_code:
            pcre2_code_free(self.re_code)
            self.re_code = NULL
        if self.use_alternative_algorithm:
            PyMem_Free(self._workspace)


cdef Result ResultFactory(
        bytes content,
        int match_count,
        pcre2_match_data*match_data,
        bint use_alternative_algorithm,
):
    cdef Result res = Result(use_alternative_algorithm=use_alternative_algorithm)
    cdef bytes substring
    cdef PCRE2_SIZE *ovector = pcre2_get_ovector_pointer(match_data)
    cdef int i

    for i in range(match_count):
        substring = content[ovector[2 * i]:ovector[2 * i + 1]]
        res.add_match(substring)

    return res


cdef class Result:
    cdef list matches
    cdef bint use_alternative_algorithm

    def __init__(self, use_alternative_algorithm=False):
        self.matches = []
        self.use_alternative_algorithm = use_alternative_algorithm

    def add_match(self, bytes substring):
        self.matches.append(substring)

    def group(self, index):
        if self.use_alternative_algorithm:
            raise NotImplementedError('Alternative algorithm cannot capture subexpressions')
        return self.matches[index]

    def groups(self):
        if self.use_alternative_algorithm:
            raise NotImplementedError('Alternative algorithm cannot capture subexpressions')
        return self.matches[1:]
