"""
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
 - protobuf shit
 - type hierarchy graphviz
 - packaging
  - tame freeze (pyinstaller? pyoxidizer?)
  - pex
 - pyenv stuff
 - ‘semi-static’ checks..? match exhaustiveness etc
  - DO NOT WANT compile-timme forced impl-all mandate but do want flake
 - d3js webservy stuff using own webservers
 - notebook stuff
 - vendoring - import rewriting
 - pycparser / pycpp
 - diffing - dc -> protofbuf gen
 - awk(pawk)/jq(jp) entrypoints
 - build-time classpath scanning (yield_importable) + codegen
  - resolve.rb paths
 - deployment, self infra, pub+priv gh -> aws, suproc-heavy (incl aws/gcloud?)
  - kubectl?
 - packing here but llvm.so dynalinking in main
 - pants
 - compose
 - dep mgmt

ast.copy_location(new_node, node)
ast.fix_missing_locations(new_node)

cmake:
 - https://cliutils.gitlab.io/modern-cmake/
 - https://github.com/awslabs/aws-lambda-cpp

https://github.com/lyft/pynamodb-mypy/tree/master/pynamodb_mypy
https://sobolevn.me/2019/08/testing-mypy-types
https://github.com/github/semantic
https://gitlab.com/coala/bears/coala-antlr/commit/abc9f3b0
https://github.com/indygreg/python-build-standalone
https://github.com/pypa/auditwheel/blob/master/auditwheel/elfutils.py
https://github.com/pypa/packaging
https://python-devtools.helpmanual.io/
https://github.com/MacPython/pandas-wheels
https://github.com/jasontrigg0/pawk
https://github.com/cookiecutter/cookiecutter/blob/1.7.0/cookiecutter/repository.py
"""
