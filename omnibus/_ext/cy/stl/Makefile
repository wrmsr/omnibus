SHELL:=/bin/bash


.PHONY: clean
clean:
	-rm -f *.so
	-rm -f gen_*
	-rm -f stl.cpp
	-rm -f stl.pyx

.PHONY: render
render:
	cat "$(shell python -c 'import Cython; print(Cython.__path__[0])')/Includes/libcpp/unordered_map.pxd" | \
		sed 's/cdef cppclass unordered_map\[T, U\]/cdef cppclass unordered_map[T, U, HASH=*,PRED=*,ALLOCATOR=*]/' | \
		sed "s/^from \./from libcpp./" \
		> gen_unordered_map.pxd

	python -m mako.cmd stl.pyx.mako > stl.pyx
