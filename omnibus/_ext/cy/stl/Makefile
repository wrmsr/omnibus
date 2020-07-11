SHELL:=/bin/bash


.PHONY: clean
clean:
	-rm -f *.so
	-rm -f gen_*
	-rm -f stl.cpp
	-rm -f stl.pyx

.PHONY: render
render:
	python -m mako.cmd stl.pyx.mako > stl.pyx
