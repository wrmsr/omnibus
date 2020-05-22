SHELL:=/bin/bash

PYTHON_VERSION:=3.8.3
PYTHON_37_VERSION:=3.7.7

PYENV_ROOT:=$(shell if [ -z "$${PYENV_ROOT}" ]; then echo "$${HOME}/.pyenv" ; else echo "$${PYENV_ROOT%/}" ; fi)
PYENV_BIN:=$(shell if [ -f "$${HOME}/.pyenv/bin/pyenv" ] ; then echo "$${HOME}/.pyenv/bin/pyenv" ; else echo pyenv ; fi)

PIP_ARGS:=

PYENV_BREW_DEPS:= \
	openssl \
	readline \
	sqlite3 \
	zlib \


ANTLR_VERSION=4.8


### Aggregates

all: build flake test test-37

venv-all: venv venv-37 docker-venv docker-venv-37

test-all: venv-all test test-37 docker-test docker-test-37

dist-all: venv-all dist dist-37 docker-dist docker-dist-37


### Clean

.PHONY: clean
clean:
	-rm -rf .cache
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	-rm -rf .venv*
	-rm -rf build
	-rm -rf dist
	-rm -rf omnibus.egg-info

	find omnibus \
		-name '*.pyc' -delete -or \
		-name '*.pyo' -delete -or \
		-name '__pycache__' -delete -or \
		-name '*.so' -delete -or \
		-name '*.dylib' -delete -or \
		-name '*.exe' -delete -or \
		-name '.revision' -delete

	if [ -d omnibus/_ext/cy ]; then \
		find omnibus/_ext/cy \
			-name '*.c' -delete -or \
			-name '*.cpp' -delete ; \
	fi


### Venvs

.PHONY: brew
brew:
	brew install $(PYENV_BREW_DEPS)

define do-venv
	if [ ! -d $(1) ] ; then \
		set -e ; \
		\
		if [ -z "$$DEBUG" ] && [ "$$(python --version)" = "Python $(2)" ] ; then \
			virtualenv $(1) ; \
		\
		else \
			PYENV_INSTALL_DIR="$(2)" ; \
			PYENV_INSTALL_FLAGS="-s -v"; \
			if [ ! -z "$$DEBUG" ] ; then \
				PYENV_INSTALL_DIR="$$PYENV_INSTALL_DIR"-debug ; \
				PYENV_INSTALL_FLAGS="$$PYENV_INSTALL_FLAGS -g" ; \
			fi ; \
			\
			if [ "$$(uname)" = "Darwin" ] && command -v brew ; then \
				PYENV_CFLAGS="" ; \
				PYENV_LDFLAGS="" ; \
				for DEP in $(PYENV_BREW_DEPS); do \
					DEP_PREFIX="$$(brew --prefix "$$DEP")" ; \
					PYENV_CFLAGS="-I$$DEP_PREFIX/include $$PYENV_CFLAGS" ; \
					PYENV_LDFLAGS="-L$$DEP_PREFIX/lib $$PYENV_LDFLAGS" ; \
				done ; \
				\
				PYTHON_CONFIGURE_OPTS="--enable-framework" ; \
				if brew --prefix tcl-tk ; then \
					TCL_TK_PREFIX="$$(brew --prefix tcl-tk)" ; \
					TCL_TK_VER="$$(brew ls --versions tcl-tk | head -n1 | egrep -o '[0-9]+\.[0-9]+')" ; \
					PYTHON_CONFIGURE_OPTS="$$PYTHON_CONFIGURE_OPTS --with-tcltk-includes='-I$$TCL_TK_PREFIX/include'" ; \
					PYTHON_CONFIGURE_OPTS="$$PYTHON_CONFIGURE_OPTS --with-tcltk-libs='-L$$TCL_TK_PREFIX/lib -ltcl$$TCL_TK_VER -ltk$$TCL_TK_VER'" ; \
				fi ; \
				\
				CFLAGS="$$PYENV_CFLAGS $$CFLAGS" \
				LDFLAGS="$$PYENV_LDFLAGS $$LDFLAGS" \
				PKG_CONFIG_PATH="$$(brew --prefix openssl)/lib/pkgconfig:$$PKG_CONFIG_PATH" \
				PYTHON_CONFIGURE_OPTS="$$PYTHON_CONFIGURE_OPTS" \
				"$(PYENV_BIN)" install $$PYENV_INSTALL_FLAGS $(2) ; \
			\
			else \
				"$(PYENV_BIN)" install $$PYENV_INSTALL_FLAGS $(2) ; \
			\
			fi ; \
			\
			"$(PYENV_ROOT)/versions/$$PYENV_INSTALL_DIR/bin/python" -m venv $(1) ; \
		fi ; \
		\
		$(1)/bin/pip install --upgrade pip setuptools wheel ; \
		$(1)/bin/pip install $(PIP_ARGS) -r requirements-dev.txt ; \
		\
		if [ -d "/Applications/PyCharm.app/Contents/helpers/pydev/" ] ; then \
			if $(1)/bin/python -c 'import sys; exit(0 if sys.version_info < (3, 7) else 1)' ; then \
				$(1)/bin/python "/Applications/PyCharm.app/Contents/helpers/pydev/setup_cython.py" build_ext --inplace ; \
			fi ; \
		fi ; \
	fi
endef

.PHONY: venv
venv:
	$(call do-venv,.venv,$(PYTHON_VERSION))

.PHONY: venv-37
venv-37:
	$(call do-venv,.venv-37,$(PYTHON_37_VERSION))


### Antlr

.PHONY: antlr
antlr:
	if [ ! -f "antlr-$(ANTLR_VERSION)-complete.jar" ] ; then \
		curl \
			--proto '=https' \
			--tlsv1.2 \
			"https://www.antlr.org/download/antlr-$(ANTLR_VERSION)-complete.jar" \
			-o "antlr-$(ANTLR_VERSION)-complete.jar" ; \
	fi

	set -e ; \
	\
	java -version ; \
	\
	find omnibus -name _antlr -type d | xargs -n 1 rm -rf ; \
	\
	for D in $$(find omnibus -name '*.g4' | xargs -n1 dirname | sort | uniq) ; do \
		echo "$$D" ; \
		\
		mkdir "$$D/_antlr" ; \
		touch "$$D/_antlr/__init__.py" ; \
		\
		for F in $$(find "$$D" -name '*.g4' -maxdepth 1 | sort) ; do \
			cp "$$F" "$$D/_antlr/"; \
		done ; \
		\
		P=$$(pwd) ; \
		for F in $$(find "$$D/_antlr" -name '*.g4' | sort) ; do \
			echo "$$F" ; \
			( \
				cd "$$D/_antlr" && \
				java \
					-jar "$$P/antlr-$(ANTLR_VERSION)-complete.jar" \
					-Dlanguage=Python3 \
					-visitor \
					$$(basename "$$F") \
			) ; \
		done ; \
		\
		find "$$D/_antlr" -name '*.g4' -delete ; \
		\
		for P in $$(find "$$D/_antlr" -name '*.py' -not -name '__init__.py') ; do \
			( \
				BUF=$$(echo -e '# flake8: noqa' && cat "$$P") ; \
				IMP=$$(echo "$$D" | tr -dc / | tr / .) ; \
				BUF=$$(echo "$$BUF" | sed "s/^from antlr4/from $$IMP.._vendor.antlr4/") ; \
				echo "$$BUF" > "$$P" \
			) ; \
		done ; \
	done


### Build

define do-build
	$(1)/bin/python setup.py build_ext --inplace
endef

.PHONY: build
build: venv
	$(call do-build,.venv)

.PHONY: build-37
build-37: venv-37
	$(call do-build,.venv-37)


### Check

.PHONY: flake
flake: venv
	.venv/bin/flake8 omnibus

.PHONY: typecheck
typecheck: venv
	.venv/bin/mypy --ignore-missing-imports omnibus | awk '{c+=1;print $$0}END{print c}'


### Test

.PHONY: test
test: build
	.venv/bin/pytest -v -n auto omnibus

.PHONY: test-37
test-37: venv-37
	.venv-37/bin/pytest -v -n auto omnibus

.PHONY: test-verbose
test-verbose: build
	.venv/bin/pytest -svvv omnibus


### Dist

define do-dist
	rm -rf build
	mkdir build
	$(eval DIST_BUILD_PYTHON:=$(shell echo "$(shell pwd)/$(1)/bin/python"))

	cp -rv \
		LICENSE \
		omnibus \
		README.md \
	\
		build/
	cp -rv \
		LICENSE-* \
	\
		build/ || :

	if [ $(2) == "1" ] ; then \
		cp setup-dev.py build/setup.py ; \
		cp MANIFEST-dev.in build/MANIFEST.in ; \
	else \
		cp setup.py build/setup.py ; \
		cp MANIFEST.in build/MANIFEST.in ; \
	fi

	find build -name '*.so' -delete
	cd build && "$(DIST_BUILD_PYTHON)" setup.py clean

	if [ ! -f "omnibus/.revision" ] ; then \
		git describe --match=NeVeRmAtCh --always --abbrev=40 --dirty > "build/omnibus/.revision" ; \
	fi

	if [ "$(1)" = ".venv" ] ; then \
		cd build && "$(DIST_BUILD_PYTHON)" setup.py sdist --formats=zip ; \
	fi

	if [ $(2) != "1" ] ; then \
		cd build && "$(DIST_BUILD_PYTHON)" setup.py bdist_wheel ; \
	fi

	if [ ! -d ./dist ] ; then \
		mkdir dist ; \
	fi
	cp build/dist/* ./dist/
endef

.PHONY: test-install
test-install: dist
	rm -rf .venv-install

	if [ "$$(python --version)" == "Python $(PYTHON_VERSION)" ] ; then \
		virtualenv .venv-install ; \
	else \
		"$(PYENV_BIN)" install -s $(PYTHON_VERSION) ; \
		"$(PYENV_ROOT)/versions/$(PYTHON_VERSION)/bin/python" -m venv .venv-install ; \
	fi ; \

	.venv-install/bin/pip install --force-reinstall $(PIP_ARGS) \
		$$(find dist/*.zip)$$(.venv-install/bin/python -c 'import setup; e=setup.EXTRAS_REQUIRE; print(("["+",".join(e)+"]") if e else "")')

	cd .venv-install && bin/python -c 'import omnibus; omnibus._test_install()'

.PHONY: dist
dist: venv
	$(call do-dist,.venv,0)

.PHONY: dist-37
dist-37: venv-37
	$(call do-dist,.venv-37,0)


### Dev

.PHONY: dist-dev
dist-dev: venv
	$(call do-dist,.venv,1)


### Publish

.PHONY:
publish: clean dist test-install
	if [ ! -z "$$(git status -s)" ] ; then \
		echo dirty ; \
		exit 1 ; \
	fi

	.venv/bin/twine upload dist/*

.PHONY: test-pypi
test-pypi:
	rm -rf .venv-pypi

	if [ "$$(python --version)" == "Python $(PYTHON_VERSION)" ] ; then \
		virtualenv .venv-pypi ; \
	else \
		"$(PYENV_BIN)" install -s $(PYTHON_VERSION) ; \
		"$(PYENV_ROOT)/versions/$(PYTHON_VERSION)/bin/python" -m venv .venv-pypi ; \
	fi ; \

	cd .venv-pypi && bin/pip install omnibus && bin/python -m omnibus.revision


### Deps

.PHONY: depupdates
dep-updates: venv
	.venv/bin/pip list -o --format=columns

.PHONY: deptree
dep-tree: test-install
	.venv/bin/pipdeptree


### Docker

.PHONY: docker-clean
docker-clean:
	(cd docker && make clean)

.PHONY: docker-stop
docker-stop:
	(cd docker && make stop)

.PHONY: docker-rmdev
docker-rmdev:
	(cd docker && make rmdev)

.PHONY: docker-reup
docker-reup:
	(cd docker && make reup)

.PHONY: docker-invalidate
docker-invalidate:
	date +%s > .dockertimestamp


### Docker Proxies

## Venvs

.PHONY: docker-clean-venv
docker-clean-venv:
	rm -rf .venv-docker
	rm -rf .venv-docker-37

.PHONY: docker-venv
docker-venv:
	./docker-dev make _docker-venv

.PHONY: docker-venv-37
docker-venv-37:
	./docker-dev make _docker-venv-37

.PHONY: _docker-venv
_docker-venv:
	$(call do-venv,.venv-docker,$(PYTHON_VERSION))

.PHONY: _docker-venv-37
_docker-venv-37:
	$(call do-venv,.venv-docker-37,$(PYTHON_37_VERSION))

## Build

.PHONY: docker-build
docker-build: docker-venv
	./docker-dev make _docker-build

.PHONY: docker-build-37
docker-build-37: docker-venv-37
	./docker-dev make _docker-build-37

.PHONY: _docker-build
_docker-build:
	$(call do-build,.venv-docker)

.PHONY: _docker-build-37
_docker-build-37:
	$(call do-build,.venv-docker-37)

## Test

.PHONY: docker-test
docker-test: docker-build
	./docker-dev .venv-docker/bin/pytest -v -n auto omnibus

.PHONY: docker-test-37
docker-test-37: docker-build-37
	./docker-dev .venv-docker-37/bin/pytest -v -n auto omnibus

## Dist

.PHONY: docker-dist
docker-dist: docker-venv
	./docker-dev make _docker-dist

.PHONY: docker-dist-37
docker-dist-37: docker-venv-37
	./docker-dev make _docker-dist-37

.PHONY: _docker-dist
_docker-dist:
	$(call do-dist,.venv-docker,0)

.PHONY: _docker-dist-37
_docker-dist-37:
	$(call do-dist,.venv-docker-37,0)
