SHELL:=/bin/bash

PROJECT:=omnibus

PYTHON_VERSION:=3.8.5
PYTHON_37_VERSION:=3.7.8
PYTHON_39_VERSION:=3.9.0rc1

PYENV_ROOT:=$(shell if [ -z "$${PYENV_ROOT}" ]; then echo "$${HOME}/.pyenv" ; else echo "$${PYENV_ROOT%/}" ; fi)
PYENV_BIN:=$(shell if [ -f "$${HOME}/.pyenv/bin/pyenv" ] ; then echo "$${HOME}/.pyenv/bin/pyenv" ; else echo pyenv ; fi)

PIP_ARGS:=

PYENV_BREW_DEPS:= \
	openssl \
	readline \
	sqlite3 \
	zlib \


ANTLR_VERSION=4.8

REQUIREMENTS_TXT=requirements-exp.txt


### Toplevel

all: venv gen build flake test test-37

venv-all: venv venv-37 docker-venv docker-venv-37

test-all: venv-all test test-37 docker-test docker-test-37

dist-all: venv-all dist dist-37 docker-dist docker-dist-37


### Clean

.PHONY: clean-build
clean-build:
	-rm -rf build
	-rm -rf dist
	-rm -rf $(PROJECT).egg-info

	find $(PROJECT) \
		\
		-name '*.dylib' -delete -or \
		-name '*.exe' -delete -or \
		-name '*.pyc' -delete -or \
		-name '*.pyo' -delete -or \
		-name '*.so' -delete -or \
		-name '.revision' -delete -or \
		-name '__pycache__' -delete -or \
		-name 'test-*.xml' -delete -or \
		\
		-name 'NeVeRmAtCh' -delete

	if [ -d $(PROJECT)/_ext/cy ]; then \
		find $(PROJECT)/_ext/cy \
			\
			-name '*.c' -delete -or \
			-name '*.cpp' -delete -or \
			\
			-name 'NeVeRmAtCh' -delete ; \
	fi

	(cd $(PROJECT)/_ext/cy/stl && $(MAKE) clean)

.PHONY: clean
clean: clean-build
	-rm -rf .cache
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	-rm -rf .venv*


### Venvs

.PHONY: brew
brew:
	brew install $(PYENV_BREW_DEPS)

define do-venv
	set -e ; \
	\
	if [ -z "$$DEBUG" ] && [ "$$(python --version)" = "Python $(2)" ] ; then \
		python -m venv $(1) ; \
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
	$(1)/bin/pip install --upgrade pip setuptools wheel
endef

define do-deps
	$(1)/bin/pip install $(PIP_ARGS) -r $(2) ; \
	\
	if [ -d "/Applications/PyCharm.app/Contents/plugins/python/helpers/pydev/" ] ; then \
		if $(1)/bin/python -c 'import sys; exit(0 if sys.version_info < (3, 7) else 1)' ; then \
			$(1)/bin/python "/Applications/PyCharm.app/Contents/plugins/python/helpers/pydev/setup_cython.py" build_ext --inplace ; \
		fi ; \
	fi
endef

.PHONY: venv
venv:
	if [ ! -d .venv ] ; then \
		$(call do-venv,.venv,$(PYTHON_VERSION)) ; \
		$(call do-deps,.venv,$(REQUIREMENTS_TXT)) ; \
	fi

.PHONY: venv-37
venv-37:
	if [ ! -d .venv-37 ] ; then \
		$(call do-venv,.venv-37,$(PYTHON_37_VERSION)) ; \
		$(call do-deps,.venv-37,$(REQUIREMENTS_TXT)) ; \
	fi

.PHONY: venv-39
venv-39:
	if [ ! -d .venv-39 ] ; then \
		$(call do-venv,.venv-39,$(PYTHON_39_VERSION)) ; \
		$(call do-deps,.venv,requirements.txt) ; \
		.venv-39/bin/pip install ipython ; \
	fi


### Gen

.PHONY: gen
gen: antlr stl
	true

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
	find $(PROJECT) -name _antlr -type d | xargs -n 1 rm -rf ; \
	\
	for D in $$(find $(PROJECT) -name '*.g4' | xargs -n1 dirname | sort | uniq) ; do \
		echo "$$D" ; \
		\
		mkdir "$$D/_antlr" ; \
		touch "$$D/_antlr/__init__.py" ; \
		\
		for F in $$(find "$$D" -maxdepth 1 -name '*.g4' | sort) ; do \
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
				BUF=$$(echo -e '# flake8: noqa\n# type: ignore' && cat "$$P") ; \
				IMP=$$(echo "$$D" | tr -dc / | tr / .) ; \
				BUF=$$(echo "$$BUF" | sed "s/^from antlr4/from $$IMP.._vendor.antlr4/") ; \
				echo "$$BUF" > "$$P" \
			) ; \
		done ; \
	done

.PHONY: stl
stl: venv
	(. .venv/bin/activate && cd $(PROJECT)/_ext/cy/stl && $(MAKE) render)


### Build

define do-build
	$(1)/bin/python setup.py build_ext --inplace
endef

.PHONY: build
build: venv gen
	$(call do-build,.venv)

.PHONY: build-37
build-37: venv-37 gen
	$(call do-build,.venv-37)


### Check

.PHONY: flake
flake: venv
	.venv/bin/flake8 $(PROJECT)

.PHONY: typecheck
typecheck: venv
	PYTHONPATH=. .venv/bin/mypy --ignore-missing-imports $(PROJECT)

.PHONY: type-ignore-vendor
type-ignore-vendor:
	# # type: ignore
	for F in $$(find $(PROJECT)/_vendor -name '*.py') ; do \
		if [ ! -s "$$F" ] ; then \
			continue ; \
		fi ; \
		if [ ! "$$(sed -n '/^# type: ignore/p;q' "$$F")" ] ; then \
			echo "$$F" ; \
			BUF=$$(cat "$$F") ; \
			(echo -e "# type: ignore" ; echo "$$BUF") > "$$F" ; \
		fi ; \
	done


### Test

.PHONY: test
test:
	.venv/bin/pytest -v -n auto $(PROJECT)

.PHONY: test-37
test-37:
	.venv-37/bin/pytest -v -n auto $(PROJECT)

.PHONY: test-verbose
test-verbose:
	.venv/bin/pytest -svvv $(PROJECT)


### Dist

define do-dist
	$(eval DIST_BUILD_DIR:=$(if $(filter "$(3)", "1"), $(shell mktemp -d -t $(PROJECT)-build-XXXXXXXXXX), build))
	echo $(DIST_BUILD_DIR)

	if [ $(DIST_BUILD_DIR) == "build" ] ; then \
		rm -rf build ; \
		mkdir build ; \
	fi

	$(eval DIST_BUILD_PYTHON:=$(shell echo "$(shell pwd)/$(1)/bin/python"))

	cp -rv \
		LICENSE \
		$(PROJECT) \
		README.md \
	\
		$(DIST_BUILD_DIR)/
	cp -rv \
		LICENSE-* \
	\
		$(DIST_BUILD_DIR)/ || :

	if [ $(2) == "1" ] ; then \
		cp setup-dev.py $(DIST_BUILD_DIR)/setup.py ; \
		cp MANIFEST-dev.in $(DIST_BUILD_DIR)/MANIFEST.in ; \
	else \
		cp setup.py $(DIST_BUILD_DIR)/setup.py ; \
		cp MANIFEST.in $(DIST_BUILD_DIR)/MANIFEST.in ; \
	fi

	find $(DIST_BUILD_DIR) -name '*.so' -delete
	cd $(DIST_BUILD_DIR) && "$(DIST_BUILD_PYTHON)" setup.py clean

	git describe --match=NeVeRmAtCh --always --abbrev=40 --dirty > "$(DIST_BUILD_DIR)/$(PROJECT)/.revision"
	git describe --match=NeVeRmAtCh --always --abbrev=40 --dirty > "$(DIST_BUILD_DIR)/$(PROJECT)/dev/.revision"

	if [ "$(1)" = ".venv" ] ; then \
		cd $(DIST_BUILD_DIR) && "$(DIST_BUILD_PYTHON)" setup.py sdist --formats=zip ; \
	fi

	if [ $(2) != "1" ] ; then \
		cd $(DIST_BUILD_DIR) && "$(DIST_BUILD_PYTHON)" setup.py bdist_wheel ; \
	fi

	if [ ! -d ./dist ] ; then \
		mkdir dist ; \
	fi
	cp $(DIST_BUILD_DIR)/dist/* ./dist/
endef

.PHONY: test-install
test-install: dist
	rm -rf .venv-install

	if [ "$$(python --version)" == "Python $(PYTHON_VERSION)" ] ; then \
		python -m venv .venv-install ; \
	else \
		"$(PYENV_BIN)" install -s $(PYTHON_VERSION) ; \
		"$(PYENV_ROOT)/versions/$(PYTHON_VERSION)/bin/python" -m venv .venv-install ; \
	fi ; \

	.venv-install/bin/pip install --force-reinstall $(PIP_ARGS) \
		$$(find dist/*.zip)$$(.venv-install/bin/python -c 'import setup; e=setup.EXTRAS_REQUIRE; print(("["+",".join(e)+"]") if e else "")')

	cd .venv-install && bin/python -c 'import $(PROJECT); $(PROJECT)._test_install()'

.PHONY: dist
dist: venv
	$(call do-dist,.venv,0,0)

.PHONY: dist-37
dist-37: venv-37
	$(call do-dist,.venv-37,0,0)


### Dev

.PHONY: dist-dev
dist-dev: venv
	$(call do-dist,.venv,1,0)


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
		python -m venv .venv-pypi ; \
	else \
		"$(PYENV_BIN)" install -s $(PYTHON_VERSION) ; \
		"$(PYENV_ROOT)/versions/$(PYTHON_VERSION)/bin/python" -m venv .venv-pypi ; \
	fi ; \

	cd .venv-pypi && bin/pip install $(PROJECT) && bin/python -m $(PROJECT).revision


### Deps

.PHONY: deps
deps: venv
	$(call do-deps,.venv,$(REQUIREMENTS_TXT))

.PHONY: deps-37
deps-37: venv
	$(call do-deps,.venv-37,$(REQUIREMENTS_TXT))

.PHONY: deps-39
deps-39: venv
	$(call do-deps,.venv-39,requirements.txt)

.PHONY: dep-freze
dep-freeze: venv
	.venv/bin/pip freeze > requirements-frz.txt

.PHONY: dep-tree
dep-tree: venv
	.venv/bin/pipdeptree

.PHONY: dep-updates
dep-updates: venv
	.venv/bin/pip list -o --format=columns


### Docker

.PHONY: docker-clean
docker-clean:
	(cd docker && $(MAKE) clean)

.PHONY: docker-stop
docker-stop:
	(cd docker && $(MAKE) stop)

.PHONY: docker-rmdev
docker-rmdev:
	(cd docker && $(MAKE) rmdev)

.PHONY: docker-reup
docker-reup:
	(cd docker && $(MAKE) reup)

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
	if [ ! -d .venv-docker ] ; then \
		$(call do-venv,.venv-docker,$(PYTHON_VERSION)) ; \
		$(call do-deps,.venv-docker,$(REQUIREMENTS_TXT)) ; \
	fi

.PHONY: _docker-venv-37
_docker-venv-37:
	if [ ! -d .venv-docker-37 ] ; then \
		$(call do-venv,.venv-docker-37,$(PYTHON_37_VERSION)) ; \
		$(call do-deps,.venv-docker-37,$(REQUIREMENTS_TXT)) ; \
	fi

## Deps

.PHONY: docker-deps
docker-deps:
	./docker-dev make _docker-deps

.PHONY: docker-deps-37
docker-deps-37:
	./docker-dev make _docker-deps-37

.PHONY: _docker-deps
_docker-deps: _docker-venv
	$(call do-deps,.venv-docker,$(REQUIREMENTS_TXT))

.PHONY: _docker-deps-37
_docker-deps-37: _docker-venv-37
	$(call do-deps,.venv-docker-37,$(REQUIREMENTS_TXT))

## Build

.PHONY: docker-build
docker-build: docker-venv
	./docker-dev make _docker-build

.PHONY: docker-build-37
docker-build-37: docker-venv-37
	./docker-dev make _docker-build-37

.PHONY: _docker-build
_docker-build: _docker-venv
	$(call do-build,.venv-docker)

.PHONY: _docker-build-37
_docker-build-37: _docker-venv-37
	$(call do-build,.venv-docker-37)

## Test

.PHONY: docker-test
docker-test: docker-build
	./docker-dev .venv-docker/bin/pytest -v -n auto $(PROJECT)

.PHONY: docker-test-37
docker-test-37: docker-build-37
	./docker-dev .venv-docker-37/bin/pytest -v -n auto $(PROJECT)

## Dist

.PHONY: docker-dist
docker-dist: docker-venv
	./docker-dev make _docker-dist

.PHONY: docker-dist-37
docker-dist-37: docker-venv-37
	./docker-dev make _docker-dist-37

.PHONY: _docker-dist
_docker-dist: _docker-venv
	$(call do-dist,.venv-docker,0,1)

.PHONY: _docker-dist-37
_docker-dist-37: _docker-venv-37
	$(call do-dist,.venv-docker-37,0,1)


### Ci

.PHONY: ci-pull
ci-pull:
	(cd docker && make ci-pull)

.PHONY: ci
ci:
	(cd docker && make ci)

.PHONY: ci-test
ci-test:
	flake8 $(PROJECT)
	python setup.py build_ext --inplace

	if [ -f test-results.xml ] ; then \
		rm test-results.xml ; \
	fi

	pytest -v -n auto --junitxml=test-results.xml $(PROJECT) && \
	\
	if [ ! -z "$$OMNIBUS_CI_OUTPUT_DIR" ] ; then \
		cp test-results.xml "$$OMNIBUS_CI_OUTPUT_DIR/test-results.xml" ; \
	fi
