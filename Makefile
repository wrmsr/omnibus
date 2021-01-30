SHELL:=/bin/bash

PROJECT:=omnibus

PYTHON_VERSION:=3.8.6
PYTHON_37_VERSION:=3.7.9
PYTHON_39_VERSION:=3.9.1
PYPY_37_VERSION:=3.7-7.3.3

PYENV_ROOT:=$(shell if [ -z "$${PYENV_ROOT}" ]; then echo "$${HOME}/.pyenv" ; else echo "$${PYENV_ROOT%/}" ; fi)
PYENV_BIN:=$(shell if [ -f "$${HOME}/.pyenv/bin/pyenv" ] ; then echo "$${HOME}/.pyenv/bin/pyenv" ; else echo pyenv ; fi)

PIP_ARGS:=

PYENV_BREW_DEPS:= \
	openssl \
	readline \
	sqlite3 \
	zlib \

BREW_DEPS:= \
	$(PYENV_BREW_DEPS) \
	graphviz \
	libyaml \
	node \
	pipx \
	protobuf \

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
		-name NeVeRmAtCh

	if [ -d $(PROJECT)/_ext/cy ]; then \
		find $(PROJECT)/_ext/cy \
			\
			-name '*.c' -delete -or \
			-name '*.cpp' -delete -or \
			\
			-name 'NeVeRmAtCh' -delete ; \
	fi

	(cd $(PROJECT)/_ext/cy && $(MAKE) clean)

.PHONY: clean
clean: clean-build
	-rm -rf .benchmarks
	-rm -rf .cache
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	-rm -rf .venv*


### Venvs

.PHONY: brew-install
brew-install:
	brew install $(BREW_DEPS)

.PHONY: brew-upgrade
brew-upgrade:
	brew install $(BREW_DEPS)

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
		$(call do-deps,.venv-39,requirements-dev.txt) ; \
	fi


### Gen

.PHONY: gen
gen: antlr cy
	true

.PHONY: antlr
antlr: venv
	.venv/bin/python -m $(PROJECT).dev.projects.antlr gen $(PROJECT) --self-vendor

.PHONY: cy
cy: venv
	(. .venv/bin/activate && cd $(PROJECT)/_ext/cy && $(MAKE) build)


### Build

define do-build
	$(1)/bin/python setup.py build_ext --inplace
endef

.PHONY: build-ext
build-ext: venv
	$(call do-build,.venv)

.PHONY: build
build: venv gen build-ext

.PHONY: build-37
build-37: venv-37 gen
	$(call do-build,.venv-37)

.PHONY: build-39
build-39: venv-39 gen
	$(call do-build,.venv-39)


### Check

.PHONY: flake
flake: venv
	.venv/bin/flake8 $(PROJECT)

.PHONY: typecheck
typecheck: venv
	PYTHONPATH=. .venv/bin/mypy $(PROJECT)

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
test: venv
	.venv/bin/pytest -v -n auto $(PROJECT)

.PHONY: test-37
test-37: venv-37
	.venv-37/bin/pytest -v -n auto $(PROJECT)

.PHONY: test-39
test-39: venv-39
	.venv-39/bin/pytest -v -n auto $(PROJECT)

.PHONY: test-verbose
test-verbose:
	.venv/bin/pytest -svvv $(PROJECT)

.PHONY: test-no-docker
test-no-docker: venv
	.venv/bin/pytest -v -n auto --no-docker $(PROJECT)


### Dist

.PHONY: test-install
test-install:
	if [ ! -d .venv-install ] ; then \
		if [ "$$(python --version)" == "Python $(PYTHON_VERSION)" ] ; then \
			python -m venv .venv-install ; \
		else \
			"$(PYENV_BIN)" install -s $(PYTHON_VERSION) ; \
			"$(PYENV_ROOT)/versions/$(PYTHON_VERSION)/bin/python" -m venv .venv-install ; \
		fi ; \
	fi

	.venv-install/bin/pip install -r requirements.txt
	.venv-install/bin/pip uninstall -y $(PROJECT)
	.venv-install/bin/python setup.py install
	cd .venv-install && bin/python -c 'import $(PROJECT); $(PROJECT)._test_install()'

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

.PHONY: test-dist
test-dist: dist
	rm -rf .venv-dist

	if [ "$$(python --version)" == "Python $(PYTHON_VERSION)" ] ; then \
		python -m venv .venv-dist ; \
	else \
		"$(PYENV_BIN)" install -s $(PYTHON_VERSION) ; \
		"$(PYENV_ROOT)/versions/$(PYTHON_VERSION)/bin/python" -m venv .venv-dist ; \
	fi ; \

	.venv-dist/bin/pip install --force-reinstall $(PIP_ARGS) \
		$$(find dist/*.zip)$$(.venv-dist/bin/python -c 'import setup; e=setup.EXTRAS_REQUIRE; print(("["+",".join(e)+"]") if e else "")')

	cd .venv-dist && bin/python -c 'import $(PROJECT); $(PROJECT)._test_install()'

.PHONY: dist
dist: venv build
	$(call do-dist,.venv,0,0)

.PHONY: dist-37
dist-37: venv-37
	$(call do-dist,.venv-37,0,0)

.PHONY: dist-39
dist-39: venv-39
	$(call do-dist,.venv-39,0,0)


### Dev

.PHONY: dist-dev
dist-dev: venv
	$(call do-dist,.venv,1,0)


### Publish

.PHONY: _publish
_publish: venv
	if [ ! -z "$$(git status -s)" ] ; then \
		echo dirty ; \
		exit 1 ; \
	fi

	.venv/bin/twine upload dist/*

.PHONY: publish
publish: clean build test dist test-dist
	$(MAKE) _publish

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
deps-37: venv-37
	$(call do-deps,.venv-37,$(REQUIREMENTS_TXT))

.PHONY: deps-39
deps-39: venv-39
	$(call do-deps,.venv-39,requirements.txt)

.PHONY: dep-freze
dep-freeze: venv
	.venv/bin/pip freeze > requirements-frz.txt

.PHONY: dep-unfreeze
dep-unfreeze: venv
	.venv/bin/pip install -r requirements-frz.txt

.PHONY: dep-tree
dep-tree: venv
	.venv/bin/pipdeptree

.PHONY: dep-updates
dep-updates: venv
	.venv/bin/pip list -o --format=columns

.PHONY: dep-autoupdate
dep-autoupdate: venv
	.venv/bin/python -m omnibus.dev.projects.deps updates -W requirements-exp.txt

.PHONY: dep-cyaml
dep-cyaml: venv
	.venv/bin/python setup.py cyaml


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
	rm -rf .venv-docker-39

.PHONY: docker-venv
docker-venv:
	./docker-dev make _docker-venv

.PHONY: docker-venv-37
docker-venv-37:
	./docker-dev make _docker-venv-37

.PHONY: docker-venv-39
docker-venv-39:
	./docker-dev make _docker-venv-39

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

.PHONY: _docker-venv-39
_docker-venv-39:
	if [ ! -d .venv-docker-39 ] ; then \
		$(call do-venv,.venv-docker-39,$(PYTHON_39_VERSION)) ; \
		$(call do-deps,.venv-docker-39,$(REQUIREMENTS_TXT)) ; \
	fi

## Deps

.PHONY: docker-deps
docker-deps:
	./docker-dev make _docker-deps

.PHONY: docker-deps-37
docker-deps-37:
	./docker-dev make _docker-deps-37

.PHONY: docker-deps-39
docker-deps-39:
	./docker-dev make _docker-deps-39

.PHONY: _docker-deps
_docker-deps: _docker-venv
	$(call do-deps,.venv-docker,$(REQUIREMENTS_TXT))

.PHONY: _docker-deps-37
_docker-deps-37: _docker-venv-37
	$(call do-deps,.venv-docker-37,$(REQUIREMENTS_TXT))

.PHONY: _docker-deps-39
_docker-deps-39: _docker-venv-39
	$(call do-deps,.venv-docker-39,$(REQUIREMENTS_TXT))

## Build

.PHONY: docker-build
docker-build: docker-venv
	./docker-dev make _docker-build

.PHONY: docker-build-37
docker-build-37: docker-venv-37
	./docker-dev make _docker-build-37

.PHONY: docker-build-39
docker-build-39: docker-venv-39
	./docker-dev make _docker-build-39

.PHONY: _docker-build
_docker-build: _docker-venv
	$(call do-build,.venv-docker)

.PHONY: _docker-build-37
_docker-build-37: _docker-venv-37
	$(call do-build,.venv-docker-37)

.PHONY: _docker-build-39
_docker-build-39: _docker-venv-39
	$(call do-build,.venv-docker-39)

## Test

.PHONY: docker-test
docker-test: docker-build
	./docker-dev .venv-docker/bin/pytest -v -n auto $(PROJECT)

.PHONY: docker-test-37
docker-test-37: docker-build-37
	./docker-dev .venv-docker-37/bin/pytest -v -n auto $(PROJECT)

.PHONY: docker-test-39
docker-test-39: docker-build-39
	./docker-dev .venv-docker-39/bin/pytest -v -n auto $(PROJECT)

## Dist

.PHONY: docker-dist
docker-dist: docker-venv
	./docker-dev make _docker-dist

.PHONY: docker-dist-37
docker-dist-37: docker-venv-37
	./docker-dev make _docker-dist-37

.PHONY: docker-dist-39
docker-dist-39: docker-venv-39
	./docker-dev make _docker-dist-39

.PHONY: _docker-dist
_docker-dist: _docker-venv
	$(call do-dist,.venv-docker,0,1)

.PHONY: _docker-dist-37
_docker-dist-37: _docker-venv-37
	$(call do-dist,.venv-docker-37,0,1)

.PHONY: _docker-dist-39
_docker-dist-39: _docker-venv-39
	$(call do-dist,.venv-docker-39,0,1)


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

	pytest -v -n auto --ci --junitxml=test-results.xml $(PROJECT) && \
	\
	if [ ! -z "$$OMNIBUS_CI_OUTPUT_DIR" ] ; then \
		cp test-results.xml "$$OMNIBUS_CI_OUTPUT_DIR/test-results.xml" ; \
	fi


### Utils

.PHONY: my-repl
my-repl: venv
	F=$$(mktemp) ; \
	echo -e "\n\
import yaml \n\
with open('docker/docker-compose.yml', 'r') as f: \n\
    dct = yaml.safe_load(f.read()) \n\
cfg = dct['services']['$(PROJECT)-mysql-master'] \n\
print('MY_USER=' + cfg['environment']['MYSQL_USER']) \n\
print('MY_PASSWORD=' + cfg['environment']['MYSQL_PASSWORD']) \n\
print('MY_PORT=' + cfg['ports'][0].split(':')[0]) \n\
" >> $$F ; \
	export $$(.venv/bin/python "$$F" | xargs) && \
	MYSQL_PWD="$$MY_PASSWORD" .venv/bin/mycli --user "$$MY_USER" --host localhost --port "$$MY_PORT"

.PHONY: pg-repl
pg-repl: venv
	F=$$(mktemp) ; \
	echo -e "\n\
import yaml \n\
with open('docker/docker-compose.yml', 'r') as f: \n\
    dct = yaml.safe_load(f.read()) \n\
cfg = dct['services']['$(PROJECT)-postgres-master'] \n\
print('PG_USER=' + cfg['environment']['POSTGRES_USER']) \n\
print('PG_PASSWORD=' + cfg['environment']['POSTGRES_PASSWORD']) \n\
print('PG_PORT=' + cfg['ports'][0].split(':')[0]) \n\
" >> $$F ; \
	export $$(.venv/bin/python "$$F" | xargs) && \
	PGPASSWORD="$$PG_PASSWORD" .venv/bin/pgcli --user "$$PG_USER" --host localhost --port "$$PG_PORT"
