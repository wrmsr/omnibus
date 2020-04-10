import functools
import inspect
import typing as ta

from ... import check
from ..types import Checker
from ..types import CheckException
from ..types import ExtraFieldParams
from ..types import SelfChecker
from ..types import SelfValidator
from ..types import Validator
from ..validation import build_default_field_validation
from .context import BuildContext
from .context import FunctionBuildContext


T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class Validation:

    def __init__(self, ctx: BuildContext) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    def create_init_builder(self, fctx: FunctionBuildContext) -> 'Validation.InitBuilder':
        return self.InitBuilder(self, fctx)

    class InitBuilder:

        def __init__(self, owner: 'Validation', fctx: FunctionBuildContext) -> None:
            super().__init__()

            self._owner = check.isinstance(owner, Validation)
            self._fctx = check.isinstance(fctx, FunctionBuildContext)

        @property
        def owner(self) -> 'Validation':
            return self._owner

        @property
        def fctx(self) -> FunctionBuildContext:
            return self._fctx

        @staticmethod
        def get_flat_fn_args(fn) -> ta.List[str]:
            argspec = inspect.getfullargspec(fn)
            if (
                    argspec.varargs or
                    argspec.varkw or
                    argspec.defaults or
                    argspec.kwonlyargs or
                    argspec.kwonlydefaults
            ):
                raise TypeError(fn)
            return list(argspec.args)

        def build_validate_lines(self) -> ta.List[str]:
            ret = []
            for fld in self.fctx.ctx.spec.fields:
                vld_md = fld.metadata.get(ExtraFieldParams, ExtraFieldParams()).validate
                if callable(vld_md):
                    ret.append(f'{self.fctx.nsb.put(vld_md)}({fld.name})')
                elif vld_md is True or (vld_md is None and self.fctx.ctx.extra_params.validate is True):
                    ret.append(f'{self.fctx.nsb.put(build_default_field_validation(fld))}({fld.name})')
                elif vld_md is False or vld_md is None:
                    pass
                else:
                    raise TypeError(vld_md)
            return ret

        def build_validator_lines(self) -> ta.List[str]:
            ret = []
            for vld in self.fctx.ctx.spec.rmro_extras_by_cls[Validator]:
                vld_args = self.get_flat_fn_args(vld.fn)
                for arg in vld_args:
                    check.in_(arg, self.fctx.ctx.spec.fields)
                ret.append(f'{self.fctx.nsb.put(vld.fn)}({", ".join(vld_args)})')
            return ret

        def build_self_validator_lines(self) -> ta.List[str]:
            ret = []
            for self_vld in self.fctx.ctx.spec.rmro_extras_by_cls[SelfValidator]:
                ret.append(f'{self.fctx.nsb.put(self_vld.fn)}({self.fctx.self_name})')
            return ret

        @staticmethod
        def build_chk_exc(chk, chk_args, *args):
            if len(chk_args) != len(args):
                raise TypeError(chk_args, args)
            raise CheckException({k: v for k, v in zip(chk_args, args)}, chk)

        def build_checker_lines(self) -> ta.List[str]:
            ret = []

            for chk in self.fctx.ctx.spec.rmro_extras_by_cls[Checker]:
                chk_args = self.get_flat_fn_args(chk.fn)
                for arg in chk_args:
                    check.in_(arg, self.fctx.ctx.spec.fields)
                bound_build_chk_exc = functools.partial(self.build_chk_exc, chk, chk_args)
                ret.append(
                    f'if not {self.fctx.nsb.put(chk.fn)}({", ".join(chk_args)}): '
                    f'raise {self.fctx.nsb.put(bound_build_chk_exc)}({", ".join(chk_args)})'
                )

            return ret

        def build_self_checker_lines(self) -> ta.List[str]:
            ret = []

            for self_chk in self.fctx.ctx.spec.rmro_extras_by_cls[SelfChecker]:
                self_chk_arg = [check.single(self.get_flat_fn_args(self_chk.fn))]
                bound_build_chk_exc = functools.partial(self.build_chk_exc, self_chk, self_chk_arg)
                ret.append(
                    f'if not {self.fctx.nsb.put(self_chk.fn)}({self.fctx.self_name}): '
                    f'raise {self.fctx.nsb.put(bound_build_chk_exc)}({self.fctx.self_name})'
                )

            return ret