SHELL:=/bin/bash


.PHONY: clean
clean:
	-rm -f *.so
	-rm -f gen_*
	-rm -f vmath.cpp
	-rm -f vmath.pyx

.PHONY: build
build:
	python -m mako.cmd vmath.pyx.mako > vmath.pyx
