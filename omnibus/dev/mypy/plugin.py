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


T = ta.TypeVar('T')


PREFIX = __package__.split('.')[0]


class ChainedPlugin(mp.Plugin):

    def __init__(self, options: mp.Options, plugins: ta.List[mp.Plugin]) -> None:
        super().__init__(options)
        self._plugins = plugins

    def set_modules(self, modules: ta.Dict[str, mn.MypyFile]) -> None:
        for plugin in self._plugins:
            plugin.set_modules(modules)

    def report_config_data(self, ctx: mp.ReportConfigContext) -> ta.Any:
        config_data = [plugin.report_config_data(ctx) for plugin in self._plugins]
        return config_data if any(x is not None for x in config_data) else None

    def get_additional_deps(self, file: mn.MypyFile) -> ta.List[ta.Tuple[int, str, int]]:
        deps = []
        for plugin in self._plugins:
            deps.extend(plugin.get_additional_deps(file))
        return deps

    def get_type_analyze_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.AnalyzeTypeContext], mt.Type]]:
        return self._find_hook(lambda plugin: plugin.get_type_analyze_hook(fullname))

    def get_function_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.FunctionContext], mt.Type]]:
        return self._find_hook(lambda plugin: plugin.get_function_hook(fullname))

    def get_method_signature_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.MethodSigContext], mt.CallableType]]:  # noqa
        return self._find_hook(lambda plugin: plugin.get_method_signature_hook(fullname))

    def get_method_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.MethodContext], mt.Type]]:
        return self._find_hook(lambda plugin: plugin.get_method_hook(fullname))

    def get_attribute_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.AttributeContext], mt.Type]]:
        return self._find_hook(lambda plugin: plugin.get_attribute_hook(fullname))

    def get_class_decorator_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.ClassDefContext], None]]:
        return self._find_hook(lambda plugin: plugin.get_class_decorator_hook(fullname))

    def get_metaclass_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.ClassDefContext], None]]:
        return self._find_hook(lambda plugin: plugin.get_metaclass_hook(fullname))

    def get_base_class_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.ClassDefContext], None]]:
        return self._find_hook(lambda plugin: plugin.get_base_class_hook(fullname))

    def get_customize_class_mro_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.ClassDefContext], None]]:
        return self._find_hook(lambda plugin: plugin.get_customize_class_mro_hook(fullname))

    def get_dynamic_class_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.DynamicClassDefContext], None]]:
        return self._find_hook(lambda plugin: plugin.get_dynamic_class_hook(fullname))

    def _find_hook(self, lookup: ta.Callable[[mp.Plugin], T]) -> ta.Optional[T]:
        for plugin in self._plugins:
            hook = lookup(plugin)
            if hook:
                return hook
        return None


class Plugin(ChainedPlugin):

    def __init__(self, options: mo.Options) -> None:
        from ...dataclasses.dev.mypy import DataclassPlugin

        super().__init__(options, [
            DataclassPlugin(options),
        ])


def plugin(version: str) -> ta.Type[mp.Plugin]:
    # max_stack = resource.getrlimit(resource.RLIMIT_STACK)[1]
    # resource.setrlimit(resource.RLIMIT_STACK, (0x1000000, max_stack))

    return Plugin
