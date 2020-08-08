"""
TODO:
 - mypy.. ‘interop’..
  - mypy-powered lint/refactor
   - will be heavily coupled to mypy ver :/
   - alt: simple resolution
 - revisit hy ast compo

- formatter
 - whatever ij does mostly
  - read .idea?
 - imports
 - two spaces after commas
 - comment wrapping
 - honor black blocks # fmt: off # fmt: on

- linter
 - whatever i use from flake8/pyflakes
 - __get__ requires owner=None
 - no super().__init__
 - honor # noqa
 - unused imports
 - light type checking via analysis?
 - using non-iterable things as iterable
 - omnibus aware (like mypy plugin but fully builtin)
  - dataclass, dispatch
  - need *simple* symbol resolution then
 - flake for redundant # noqa's lol

- analysis
 - type inf, sym resolution
 - query language

- refactorer
 - should basically be just user definable throwaway formatter rules
 - https://ollef.github.io/blog/posts/query-based-compilers.html

REFS:
 - https://www.python.org/dev/peps/pep-0008/
 - https://github.com/psf/black/blob/master/docs/the_black_code_style.md
 - https://github.com/timothycrosley/isort
 - https://github.com/python/cpython/tree/master/Lib/lib2to3/fixes
 - https://pylint.readthedocs.io/en/latest/technical_reference/features.html
 - https://github.com/PyCQA/pyflakes/blob/master/pyflakes/checker.py
"""