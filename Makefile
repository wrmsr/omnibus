SHELL:=/bin/bash

PYTHON_VERSION:=3.7.2

PYENV_ROOT:=$(shell if [ -z "$${PYENV_ROOT}" ]; then echo "$${HOME}/.pyenv" ; else echo "$${PYENV_ROOT%/}" ; fi)
PYENV_BIN:=$(shell if [ -f "$${HOME}/.pyenv/bin/pyenv" ] ; then echo "$${HOME}/.pyenv/bin/pyenv" ; else echo pyenv ; fi)

PIP_ARGS:=

PYENV_BREW_DEPS:= \
	openssl \
	readline \
	sqlite3 \
	zlib \

all: build test test_install

.PHONY: clean
clean:
	-rm -rf .cache
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	-rm -rf .venv
	-rm -rf .venv-install
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

.PHONY: brew
brew:
	brew install $(PYENV_BREW_DEPS)

.PHONY: venv
venv:
	if [ ! -d .venv ] ; then \
		set -e ; \
		\
		if [ -z "$$DEBUG" ] && [ "$$(python --version)" = "Python $(PYTHON_VERSION)" ] ; then \
			virtualenv .venv ; \
		else \
			PYENV_INSTALL_DIR="$(PYTHON_VERSION)" ; \
			PYENV_INSTALL_FLAGS="-s -v"; \
			if [ ! -z "$$DEBUG" ] ; then \
				PYENV_INSTALL_DIR="$$PYENV_INSTALL_DIR"-debug ; \
				PYENV_INSTALL_FLAGS="$$PYENV_INSTALL_FLAGS -g" ; \
			fi ; \
			if [ "$$(uname)" = "Darwin" ] && command -v brew ; then \
				PYENV_CFLAGS="" ; \
				PYENV_LDFLAGS="" ; \
				for DEP in $(PYENV_BREW_DEPS); do \
					PYENV_CFLAGS="-I$$(brew --prefix "$$DEP")/include $$PYENV_CFLAGS" ; \
					PYENV_LDFLAGS="-L$$(brew --prefix "$$DEP")/lib $$PYENV_LDFLAGS" ; \
				done ; \
				CFLAGS="$$PYENV_CFLAGS $$CFLAGS" \
				LDFLAGS="$$PYENV_LDFLAGS $$LDFLAGS" \
				PKG_CONFIG_PATH="$$(brew --prefix openssl)/lib/pkgconfig:$$PKG_CONFIG_PATH" \
				$(PYENV_BIN) install $$PYENV_INSTALL_FLAGS $(PYTHON_VERSION) ; \
			else \
				$(PYENV_BIN) install $$PYENV_INSTALL_FLAGS $(PYTHON_VERSION) ; \
			fi ; \
			virtualenv -p "$(PYENV_ROOT)/versions/$$PYENV_INSTALL_DIR/bin/python" .venv ; \
		fi ; \
		\
		.venv/bin/pip install --upgrade pip setuptools ; \
		.venv/bin/pip install $(PIP_ARGS) -r requirements-dev.txt ; \
		\
		if [ -d "/Applications/PyCharm.app/Contents/helpers/pydev/" ] ; then \
			if .venv/bin/python -c 'import sys; exit(0 if sys.version_info < (3, 7) else 1)' ; then \
				.venv/bin/python "/Applications/PyCharm.app/Contents/helpers/pydev/setup_cython.py" build_ext --inplace ; \
			fi ; \
		fi ; \
	fi

.PHONY: ext
ext: venv
	.venv/bin/python setup.py build_ext --inplace

.PHONY: build
build: ext

.PHONY: flake
flake: venv
	.venv/bin/flake8 omnibus

.PHONY: typecheck
typecheck: venv
	.venv/bin/mypy --ignore-missing-imports omnibus | awk '{c+=1;print $$0}END{print c}'

.PHONY: test
test: build
	.venv/bin/pytest -v omnibus

.PHONY: test_verbose
test_verbose: build
	.venv/bin/pytest -svvv omnibus

.PHONY: dist
dist: build flake test
	rm -rf dist

	$(eval DIST_BUILD_DIR:=$(shell mktemp -d))
	$(eval DIST_BUILD_PYTHON:=$(realpath .venv/bin/python))

	cp -rv \
		setup.py \
		README.md \
		MANIFEST.in \
		omnibus \
	\
		"$(DIST_BUILD_DIR)"

	if [ ! -f "omnibus/.revision" ] ; then \
		git describe --match=NeVeRmAtCh --always --abbrev=40 --dirty > "$(DIST_BUILD_DIR)/omnibus/.revision" ; \
	fi

	cd "$(DIST_BUILD_DIR)" && "$(DIST_BUILD_PYTHON)" setup.py sdist --formats=zip
	cd "$(DIST_BUILD_DIR)" && "$(DIST_BUILD_PYTHON)" setup.py bdist_wheel
	cp -rv "$(DIST_BUILD_DIR)/dist" ./

.PHONY:
upload: clean dist
	if [ -z $(git status -s) ] ; then \
		echo dirty ; \
		exit 1 ; \
	fi

	.venv/bin/twine upload dist/*

.PHONY: test_install
test_install: dist
	rm -rf .venv-install

	if [ "$$(python --version)" == "Python $(PYTHON_VERSION)" ] ; then \
		virtualenv .venv-install ; \
	else \
		$(PYENV_BIN) install -s $(PYTHON_VERSION) ; \
		virtualenv -p $(PYENV_ROOT)/versions/$(PYTHON_VERSION)/bin/python .venv-install ; \
	fi ; \

	.venv-install/bin/pip install --force-reinstall $(PIP_ARGS) \
		$$(find dist/*.zip)$$(.venv-install/bin/python -c 'import setup;e=setup.EXTRAS_REQUIRE;print(("["+",".join(e)+"]") if e else "")')

	cd .venv-install && bin/python -c 'import omnibus; omnibus._test_install()'

.PHONY: depupdates
depupdates: venv
	.venv/bin/pip list -o --format=columns

.PHONY: deptree
deptree: test_install
	.venv-install/bin/pip install pipdeptree
	echo ; echo ; echo
	.venv-install/bin/pipdeptree

.PHONY: docker_invalidate
docker_invalidate:
	date +%s > .dockertimestamp
