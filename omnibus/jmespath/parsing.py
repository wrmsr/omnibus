from . import nodes as n
from .. import check
from .._vendor import antlr4
from .antlr.JmespathLexer import JmespathLexer
from .antlr.JmespathParser import JmespathParser
from .antlr.JmespathVisitor import JmespathVisitor


class _ParseVisitor(JmespathVisitor):

    _chainedNode: n.Node = None

    def createProjectionIfChained(self, node):
        if self._chainedNode is not None:
            node = n.Sequence([node, n.Project(self._chainedNode)])
            self._chainedNode = None
        return node

    def createSequenceIfChained(self, node):
        if self._chainedNode is not None:
            node = n.Sequence([node, self._chainedNode])
            self._chainedNode = None
        return node

    def nonChainingVisit(self, tree):
        stashedNextNode = self._chainedNode
        self._chainedNode = None
        result = self.createSequenceIfChained(self.visit(tree))
        self._chainedNode = stashedNextNode
        return result

    def aggregateResult(self, aggregate, nextResult):
        check.none(aggregate)
        return check.not_none(nextResult)

    def visitSingleExpression(self, ctx: JmespathParser.SingleExpressionContext):
        return self.visit(ctx.expression())

    def visitPipeExpression(self, ctx: JmespathParser.PipeExpressionContext):
        right = self.visit(ctx.expression(1))
        left = self.visit(ctx.expression(0))
        return n.Sequence([left, right])

    def visitIdentifierExpression(self, ctx: JmespathParser.IdentifierExpressionContext):
        return self.visit(ctx.identifier())

    def visitNotExpression(self, ctx: JmespathParser.NotExpressionContext):
        return n.Negate(self.visit(ctx.expression()))

    def visitRawStringExpression(self, ctx: JmespathParser.RawStringExpressionContext):
        # FIXME: shared escaping with tree (core.util.StringEscaping) - really, in tok.util for java/sql?
        return n.String(ctx.RAW_STRING().getText())

    def visitComparisonExpression(self, ctx: JmespathParser.ComparisonExpressionContext):
        cmp = n.Compare.Op._by_value[ctx.COMPARATOR().getText()]
        right = self.nonChainingVisit(ctx.expression(1))
        left = self.nonChainingVisit(ctx.expression(0))
        return n.Compare(cmp, left, right)

    def visitParenExpression(self, ctx: JmespathParser.ParenExpressionContext):
        return self.createSequenceIfChained(self.nonChainingVisit(ctx.expression()))

    def visitBracketExpression(self, ctx: JmespathParser.BracketExpressionContext):
        result = self.visit(ctx.bracketSpecifier())
        if result is None:
            result = self._chainedNode
            self._chainedNode = None
        return result

    def visitOrExpression(self, ctx: JmespathParser.OrExpressionContext):
        left = self.nonChainingVisit(ctx.expression(0))
        right = self.nonChainingVisit(ctx.expression(1))
        return self.createSequenceIfChained(n.Or(left, right))

    def visitChainExpression(self, ctx: JmespathParser.ChainExpressionContext):
        self._chainedNode = self.visit(ctx.chainedExpression())
        return self.createSequenceIfChained(self.visit(ctx.expression()))

    def visitAndExpression(self, ctx: JmespathParser.AndExpressionContext):
        left = self.nonChainingVisit(ctx.expression(0))
        right = self.nonChainingVisit(ctx.expression(1))
        return self.createSequenceIfChained(n.And(left, right))

    def visitWildcardExpression(self, ctx: JmespathParser.WildcardExpressionContext):
        return self.visit(ctx.wildcard())

    def visitBracketedExpression(self, ctx: JmespathParser.BracketedExpressionContext):
        chainAfterExpression = self.visit(ctx.bracketSpecifier())
        expression = self.createSequenceIfChained(self.visit(ctx.expression()))
        self._chainedNode = chainAfterExpression
        return self.createSequenceIfChained(expression)

    def visitWildcard(self, ctx: JmespathParser.WildcardContext):
        return self.createProjectionIfChained(n.FlattenObject())

    def visitBracketIndex(self, ctx: JmespathParser.BracketIndexContext):
        index = int(ctx.SIGNED_INT().getText())
        self._chainedNode = self.createSequenceIfChained(n.Index(index))
        return None

    def visitBracketStar(self, ctx: JmespathParser.BracketStarContext):
        projection = n.Current() if self._chainedNode is None else self._chainedNode
        self._chainedNode = n.Project(projection)
        return None

    def visitBracketSlice(self, ctx: JmespathParser.BracketSliceContext):
        start = None
        stop = None
        step = None
        sliceCtx = ctx.slice()
        if sliceCtx.start is not None:
            start = int(sliceCtx.start.getText())
        if sliceCtx.stop is not None:
            stop = int(sliceCtx.stop.getText())
        if sliceCtx.step is not None:
            step = int(sliceCtx.step.getText())
            if step == 0:
                raise ValueError
        self._chainedNode = self.createProjectionIfChained(n.Slice(start, stop, step))
        return None

    def visitBracketFlatten(self, ctx: JmespathParser.BracketFlattenContext):
        return self.createProjectionIfChained(n.FlattenArray())

    def visitSelect(self, ctx: JmespathParser.SelectContext):
        self._chainedNode = self.createProjectionIfChained(n.Selection(self.nonChainingVisit(ctx.expression())))
        return None

    def visitMultiSelectList(self, ctx: JmespathParser.MultiSelectListContext):
        lst = []
        for i in range(len(ctx.expression())):
            lst.append(self.nonChainingVisit(ctx.expression(i)))
        return self.createSequenceIfChained(n.CreateArray(lst))

    def visitMultiSelectHash(self, ctx: JmespathParser.MultiSelectHashContext):
        dct = {}
        for i in range(len(ctx.keyvalExpr())):
            kvCtx = ctx.keyvalExpr(i)
            # FIXME: unquote?
            key = kvCtx.identifier().getText()
            value = self.nonChainingVisit(kvCtx.expression())
            dct[key] = value
        return self.createSequenceIfChained(n.CreateObject(dct))

    def visitNameParameter(self, ctx: JmespathParser.NameParameterContext):
        return n.Parameter(n.Parameter.NameTarget(ctx.NAME().getText()))

    def visitNumberParameter(self, ctx: JmespathParser.NumberParameterContext):
        return n.Parameter(n.Parameter.NumberTarget(int(ctx.INT().getText())))

    def visitFunctionExpression(self, ctx: JmespathParser.FunctionExpressionContext):
        name = ctx.NAME().getText()
        args = []
        for i in range(len(ctx.functionArg())):
            args.append(self.nonChainingVisit(ctx.functionArg(i)))
        return self.createSequenceIfChained(n.FunctionCall(name, args))

    def visitCurrentNode(self, ctx: JmespathParser.CurrentNodeContext):
        if self._chainedNode is None:
            return n.Current()
        else:
            result = self._chainedNode
            self._chainedNode = None
            return result

    def visitExpressionType(self, ctx: JmespathParser.ExpressionTypeContext):
        expression = self.createSequenceIfChained(self.visit(ctx.expression()))
        return n.ExpressionRef(expression)

    def visitLiteral(self, ctx: JmespathParser.LiteralContext):
        # visit(ctx.jsonValue())
        # FIXME: unescape
        string = ctx.jsonValue().getText()
        return n.JsonLiteral(string)

    def visitIdentifier(self, ctx: JmespathParser.IdentifierContext):
        # FIXME: unquote
        return self.createSequenceIfChained(n.Property(ctx.getText()))


def parse(buf: str) -> n.Node:
    lexer = JmespathLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = JmespathParser(stream)

    visitor = _ParseVisitor()
    return visitor.visit(parser.singleExpression())
