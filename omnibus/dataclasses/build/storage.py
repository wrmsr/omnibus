from ... import check
from .context import BuildContext


class Storage:

    def __init__(self, ctx: BuildContext) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    @properties.cached
    def init_fields(self) -> ta.List[dc.Field]:
        return [f for f in self.fields if get_field_type(f) in (FieldType.INSTANCE, FieldType.INIT)]

    def install_field_attrs(self) -> None:
        for f in self.fields:
            setattr(self.ctx.cls, f.name, f)

    def build_field_init_lines(self, locals: ta.Dict[str, ta.Any]) -> ta.List[str]:
        ret = []
        for f in self.init_fields:
            line = field_init(f, self.ctx.params.frozen, locals, self.self_name)
            # line is None means that this field doesn't require initialization (it's a pseudo-field).  Just skip it.
            if line:
                ret.append(line)
        return ret

