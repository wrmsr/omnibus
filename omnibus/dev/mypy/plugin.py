"""
TODO:
 - dataclasses
 - dispatch (class/property)
 - async/await ugh - require ta.cast(None) or smth
 - no_bool (+ runtime) - sqla bindparam equiv,
  - mypy-time virtual abc registration - register MethodType/FunctionType as NoBool, force explicit is_null
  - generic machinery working on __bool__
  - NoStrSeq, NoStrIter
  - NotIterable no_iter_set
  - usecase is enforcing callees not defensively copying (when coll will be mutating and that is **intended**)
 - NoDiscard
 - Raises - force handle

https://mypy-lang.blogspot.com/2019/03/
https://github.com/python/mypy/wiki/Type-Checker
https://github.com/python/mypy/wiki/Semantic-Analyzer

https://github.com/apache/airflow/pull/8145
https://github.com/samuelcolvin/pydantic/blob/master/pydantic/mypy.py
https://github.com/seandstewart/typical/blob/master/typic/mypy.py
https://github.com/lyft/pynamodb-mypy/tree/master/pynamodb_mypy
https://sobolevn.me/2019/08/testing-mypy-types
https://github.com/apache/airflow/blob/7d69987eddd0d5793339ccfd272bac8721d95894/airflow/mypy/plugin/decorators.py
https://github.com/leinardi/mypy-pycharm

mypy.plugin.dataclasses:dataclass_class_maker_callback

https://github.com/python/mypy/issues/1862
"""
import resource  # noqa
import typing as ta

import mypy.nodes as mn
import mypy.options as mo
import mypy.plugin as mp
import mypy.types as mt

from ... import check


PREFIX = __package__.split('.')[0]


class Plugin(mp.Plugin):

    def __init__(self, options: mo.Options) -> None:
        super().__init__(options)

    def get_type_analyze_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.AnalyzeTypeContext], mt.Type]]:
        return super().get_type_analyze_hook(fullname)

    def get_function_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.FunctionContext], mt.Type]]:
        return super().get_function_hook(fullname)

    def get_method_signature_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.MethodSigContext], mt.CallableType]]:  # noqa
        return super().get_method_signature_hook(fullname)

    def get_method_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.MethodContext], mt.Type]]:
        return super().get_method_hook(fullname)

    def get_attribute_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.AttributeContext], mt.Type]]:
        return super().get_attribute_hook(fullname)

    def get_class_decorator_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.ClassDefContext], None]]:
        if fullname in [
            PREFIX + '.dataclasses.api.dataclass',
            PREFIX + '.dev.mypy.tests.dcs.my_dataclass',
        ]:
            from mypy.plugins import dataclasses
            return dataclasses.dataclass_class_maker_callback

        return None

    def get_base_class_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.ClassDefContext], None]]:
        stn = self.lookup_fully_qualified(fullname)
        if stn is not None:
            if isinstance(stn.node, mn.TypeInfo):
                mro = check.isinstance(stn.node, mn.TypeInfo).mro
                if any(bc.fullname == PREFIX + '.dataclasses.metaclass.Data' for bc in mro):
                    from mypy.plugins import dataclasses
                    return dataclasses.dataclass_class_maker_callback

        return None


def plugin(version: str) -> ta.Type[mp.Plugin]:
    # max_stack = resource.getrlimit(resource.RLIMIT_STACK)[1]
    # resource.setrlimit(resource.RLIMIT_STACK, (0x1000000, max_stack))

    return Plugin
