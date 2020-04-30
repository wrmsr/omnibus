"""  # noqa
DECREE:
 - *DEPLESS*.
 - Dev vs 'Main' - dev = everything not shipped to prod

FIXME:
 - fix req-dev.txt? keep depless? already non-mako tmpl in main for nginx..
 - ** common test code goes in here and is not stripped, usable by consumers**

TODO:
 - tpch
 - mypy
 - twine
 - project gens (cy/rs/cc)
 - dev helping fuse stuff
 - venv helpers
 - makefile shit
 - dockerfiles
 - cmake - https://gist.github.com/wrmsr/b36337aaf2fda33faf092454a106fda6 + FT gen_cmake stuff
 - cargo stuff
 - pycharm interop (but runtime pydevd still in core)
 - gh shit
 - type hierarchy graphviz
  - + skeletonnize / stub / mock
 - pyo3 autobinder? rocksdb, v8, luajit
 - pyenv stuff
 - ‘semi-static’ checks..? match exhaustiveness etc
  - DO NOT WANT compile-timme forced impl-all mandate but do want flake
 - d3js webservy stuff using own webservers
 - notebook stuff
 - vendoring - import rewriting
 - pycparser / pycpp
 - diffing - dc -> protofbuf gen
 - build-time classpath scanning (yield_importable) + codegen
  - resolve.rb paths
 - deployment, self infra, pub+priv gh -> aws, suproc-heavy (incl aws/gcp?)
  - awscli/gcloud cli expect vs libs
  - kubectl?
  - docean/linode?
  - aws/gcp have runtime components, do/linode don't?
  - lol fuck heroku
  - https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/compute/api
 - packing here but llvm.so dynalinking in main
 - pants
 - compose
 - dep mgmt
 - hypothesis
 - https://github.com/commercialhaskell/stack/blob/master/src/Stack/New.hs
 - astor / https://gist.github.com/treo/1250562
  - https://github.com/psf/black - mine, not use
  - yapf?
  - these all suck - lib2to3?
 - om entrypoint
 - jupyter
 - clang bindings

DEPS:
 - dep version security tool.. hash verification
 - take over requirements.txt, or tack on hash (hot comment? rewritten in place?)
 - prob hook into dep resolution
 - might be safer to treat like cli, REALLY dangerous code
 - forbid external dls?
 - https://warehouse.readthedocs.io/api-reference/json/
 - https://github.com/pypa/pipfile ?
 - https://github.com/pypa/pipenv ugh
 - holy hell that vendor dir
 - https://github.com/indygreg/PyOxidizer/blob/a9f7356b9e9464ae4917a41123ff0d0ca8777694/pyoxidizer/src/py_packaging/packaging_tool.rs#L25
 - https://github.com/jazzband/pip-tools

PKG:
 - tame freeze (pyinstaller? pyoxidizer?)
  - incl/dist in dev support machinery to build pyox bins
 - pex
 - beeware briefcase?
 - prob gonna wanna xz self for pyox lam lol - llvm 20M z 13M xz
  - w/ numpy gonna crack it no matter what - tool up ‘unpacking’? bundled setup?
  - lol, hybrid venv  - THE OMNIBUS that venvs itself
  - hm, already have setuptools/pip and venv is now builtin..
  - no actually, pyox strips?


ast.copy_location(new_node, node)
ast.fix_missing_locations(new_node)

cmake:
 - https://cliutils.gitlab.io/modern-cmake/
 - https://github.com/awslabs/aws-lambda-cpp

https://github.com/joerick/cibuildwheel
https://github.com/lyft/pynamodb-mypy/tree/master/pynamodb_mypy
https://sobolevn.me/2019/08/testing-mypy-types
https://github.com/github/semantic
https://gitlab.com/coala/bears/coala-antlr/commit/abc9f3b0
https://github.com/indygreg/python-build-standalone
https://github.com/pypa/auditwheel/blob/master/auditwheel/elfutils.py
https://github.com/pypa/wheel
https://github.com/pypa/packaging
https://github.com/pypa/twine
https://github.com/pypa/pipenv/tree/master/pipenv
https://python-devtools.helpmanual.io/
https://github.com/MacPython/pandas-wheels
https://github.com/cookiecutter/cookiecutter/blob/1.7.0/cookiecutter/repository.py
https://github.com/tmrts/boilr
https://gitlab.com/rekodah/hrep
"""
