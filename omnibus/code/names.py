"""
TODO:
 - releaseable names
"""
import string
import typing as ta

from .. import check
from ..collections.identity import IdentityKeyDict


NameGenerator = ta.Callable[..., str]


class NameGeneratorImpl:

    DEFAULT_PREFIX = '_'

    def __init__(
            self,
            *,
            unavailable_names: ta.Iterable[str] = None,
            global_prefix: str = None,
            use_global_prefix_if_present: bool = False,
            add_global_prefix_before_number: bool = False,
    ) -> None:
        super().__init__()

        check.arg(not isinstance(unavailable_names, str))
        self._names = {check.isinstance(n, str) for n in (unavailable_names or [])}
        self._global_prefix = global_prefix if global_prefix is not None else self.DEFAULT_PREFIX
        self._use_global_prefix_if_present = bool(use_global_prefix_if_present)
        self._add_global_prefix_before_number = bool(add_global_prefix_before_number)

        self._name_counts: ta.Dict[str, int] = {}

    def __call__(self, prefix: str = '') -> str:
        if self._use_global_prefix_if_present and prefix.startswith(self._global_prefix):
            base_name = prefix
        else:
            base_name = self._global_prefix + prefix

        base_count = -1
        if base_name[-1] in string.digits:
            i = len(base_name) - 2
            while i >= 0 and base_name[i] in string.digits:
                i -= 1
            i += 1
            base_count = int(base_name[i:])
            base_name = base_name[:i]

        if self._add_global_prefix_before_number:
            if not (self._use_global_prefix_if_present and base_name.endswith(self._global_prefix)):
                base_name += self._global_prefix

        if base_count >= 0:
            count = self._name_counts.setdefault(base_name, 0)
            if base_count > count:
                self._name_counts[base_name] = base_count

        while True:
            count = self._name_counts.get(base_name, 0)
            self._name_counts[base_name] = count + 1
            name = base_name + str(count)
            if name not in self._names:
                return name


name_generator = NameGeneratorImpl


class NamespaceBuilder(ta.Mapping[str, ta.Any]):

    def __init__(
            self,
            *,
            unavailable_names: ta.Iterable[str] = None,
            name_generator: NameGenerator = None,
    ) -> None:
        super().__init__()

        self._unavailable_names = {
            check.isinstance(n, str)
            for n in (check.not_isinstance(unavailable_names, str) or [])
        }
        self._name_generator = check.callable(name_generator) if name_generator is not None else \
            NameGeneratorImpl(unavailable_names=self._unavailable_names, use_global_prefix_if_present=True)

        self._dct: ta.MutableMapping[str, ta.Any] = {}
        self._dedupe_dct: ta.MutableMapping[ta.Any, str] = IdentityKeyDict()

    @property
    def unavailable_names(self) -> ta.AbstractSet[str]:
        return self._unavailable_names

    @property
    def name_generator(self) -> NameGenerator:
        return self._name_generator

    def __getitem__(self, k: str) -> ta.Any:
        return self._dct[k]

    def __len__(self):
        return len(self._dct)

    def __iter__(self) -> ta.Iterable[str]:
        return iter(self._dct)

    def items(self) -> ta.Iterable[ta.Tuple[str, ta.Any]]:
        return self._dct.items()

    def put(
            self,
            value: ta.Any,
            name: str = None,
            *,
            exact: bool = False,
            dedupe: bool = False,
    ) -> str:
        check.arg(not (name is None and exact))
        if name is not None:
            check.isinstance(name, str)

        if dedupe:
            try:
                return self._dedupe_dct[value]
            except KeyError:
                pass

        if name is not None:
            if name not in self._unavailable_names:
                try:
                    existing = self._dct[name]
                except KeyError:
                    self._dct[name] = value
                    if dedupe:
                        self._dedupe_dct[value] = name
                    return name
                else:
                    if existing is value:
                        return name
            if exact:
                raise KeyError(name)

        gen_name = self._name_generator(name or '')
        check.not_in(gen_name, self._dct)
        self._dct[gen_name] = value
        if dedupe:
            self._dedupe_dct[value] = gen_name
        return gen_name
