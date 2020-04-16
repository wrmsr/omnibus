"""
TODO:
 - null/true/false - disambiguate quoted v unquoted
 - include
 - triplequote
 - optional refs ${?a.b}
 - += syntax to append elements to arrays, path += "/bin"
 - merge
 - origin
 - conversion of numerically-index objects to arrays
 - conversions: units, duration, sizes
 - comment recording

https://github.com/lightbend/config#schemas-and-validation
https://github.com/lightbend/config/blob/master/HOCON.md
"""
import typing as ta

from ..._vendor import antlr4

from ... import check
from .antlr.HoconLexer import HoconLexer
from .antlr.HoconListener import HoconListener
from .antlr.HoconParser import HoconParser
from .types import CompoundValue
from .types import NumberValue
from .types import ObjectValue
from .types import ReferenceValue
from .types import StringValue
from .types import Value
from .utils import wrap_value


class _ParseListener(HoconListener):

    def __init__(
            self,
            stream: antlr4.BufferedTokenStream.BufferedTokenStream,
            parser: HoconParser
    ) -> None:
        super().__init__()

        self._stream = stream
        self._parser = parser

        self._stack: ta.List[ta.Union[dict, list]] = [{}]
        self._compound: ta.List[Value] = None

    @classmethod
    def _reference_path(cls, path: str) -> str:
        if path.startswith('${') and path.endswith('}'):
            return path[2:-1]
        else:
            return path

    @classmethod
    def _strip_string_quotes(cls, src: str) -> str:
        ret = src
        if ret[0] == '"' or ret[0] == "'":
            ret = ret[1:-1]
        return ret

    @classmethod
    def _path_prefix(cls, path: ta.List[str]) -> ta.Tuple[ta.List[str], str]:
        if len(path) == 1:
            return [], path[0]
        else:
            return path[:-1], path[-1]

    def Obj_set(self, obj: dict, path: str, value: ta.Any) -> None:
        prefix, key = self._path_prefix(path.split('.'))
        for pkey in prefix:
            obj = obj.setdefault(pkey, {})
        obj[key] = value

    def enterObjectData(self, ctx: HoconParser.ObjectDataContext):
        self._stack.append({})

    def exitObjectData(self, ctx: HoconParser.ObjectDataContext):
        value = self._stack.pop()
        self.Obj_set(self._stack[-1], ctx.key().getText(), value)

    def exitV_string(self, ctx: HoconParser.V_stringContext):
        self._compound.append(StringValue(self._strip_string_quotes(ctx.STRING().getText())))

    def exitV_rawstring(self, ctx: HoconParser.V_rawstringContext):
        self._compound.append(StringValue(self._strip_string_quotes(ctx.rawstring().getText())))

    def exitV_reference(self, ctx: HoconParser.V_referenceContext):
        self._compound.append(ReferenceValue(self._reference_path(self._strip_string_quotes(ctx.REFERENCE().getText()))))  # noqa

    def enterStringData(self, ctx: HoconParser.StringDataContext):
        self._compound = check.replacing_none(self._compound, [])

    def exitStringData(self, ctx: HoconParser.StringDataContext):
        if self._compound is not None:
            if any(isinstance(v, ReferenceValue) for v in self._compound):
                self.Obj_set(self._stack[-1], ctx.key().getText(), CompoundValue(tuple(self._compound)))
            else:
                self.Obj_set(self._stack[-1], ctx.key().getText(), StringValue(''.join(v.value for v in self._compound)))  # noqa
            self._compound = None
        else:
            self.Obj_set(self._stack[-1], ctx.key().getText(), StringValue(self._strip_string_quotes(ctx.string_value().getText())))  # noqa

    def exitNumberData(self, ctx: HoconParser.NumberDataContext):
        self.Obj_set(self._stack[-1], ctx.key().getText(), NumberValue(ctx.NUMBER().getText()))

    def exitReferenceData(self, ctx: HoconParser.ReferenceDataContext):
        self.Obj_set(self._stack[-1], ctx.key().getText(), ReferenceValue(ctx.REFERENCE().getText()))

    def enterArrayData(self, ctx: HoconParser.ArrayDataContext):
        self._stack.append([])

    def exitArrayData(self, ctx: HoconParser.ArrayDataContext):
        value = self._stack.pop()
        self.Obj_set(self._stack[-1], ctx.key().getText(), value)

    def enterArrayArray(self, ctx: HoconParser.ArrayArrayContext):
        self._stack.append([])

    def exitArrayArray(self, ctx: HoconParser.ArrayArrayContext):
        value = self._stack.pop()
        self._stack[-1].append(value)

    def enterArrayString(self, ctx: HoconParser.ArrayStringContext):
        self._compound = check.replacing_none(self._compound, [])

    def exitArrayString(self, ctx: HoconParser.ArrayStringContext):
        if self._compound is not None:
            self._stack[-1].append(CompoundValue(tuple(self._compound)))
            self._compound = None
        else:
            self._stack[-1].append(StringValue(self._strip_string_quotes(ctx.string_value().getText())))

    def exitArrayNumber(self, ctx: HoconParser.ArrayNumberContext):
        self._stack[-1].append(NumberValue(ctx.NUMBER().getText()))

    def enterArrayObj(self, ctx: HoconParser.ArrayObjContext):
        self._stack.append({})

    def exitArrayObj(self, ctx: HoconParser.ArrayObjContext):
        value = self._stack.pop()
        self._stack[-1].append(value)


def parse(buf: str) -> ObjectValue:
    lexer = HoconLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = HoconParser(stream)
    hocon = parser.hocon()

    listener = _ParseListener(stream, parser)

    walker = antlr4.ParseTreeWalker()
    walker.walk(listener, hocon)

    check.state(listener._compound is None)
    check.state(len(listener._stack) == 1)
    return check.isinstance(wrap_value(listener._stack[0]), ObjectValue)
