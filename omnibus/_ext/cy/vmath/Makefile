SHELL:=/bin/bash


.PHONY: clean
clean:
	-rm -f *.so
	-rm -f gen_*
	-rm -f vmath.cpp
	-rm -f vmath.pyx

.PHONY: build
build:
	PYTHONPATH=$$(realpath ../../../..) python -m $$(pwd | rev | cut -d '/' -f1-4 | rev | tr -s '/' '.')._gen > vmath.pyx
