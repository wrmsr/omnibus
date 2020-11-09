# type: ignore
#
# Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root.
#
from io import StringIO
import typing as ta

from .._vendor.antlr4.atn.ATN import ATN
from .._vendor.antlr4.error.Errors import IllegalStateException
from .._vendor.antlr4.Recognizer import Recognizer
from .._vendor.antlr4.RuleContext import RuleContext


class SemanticContext:
    NONE = None

    def eval(self, parser: Recognizer, outerContext: RuleContext) -> bool:
        raise NotImplementedError

    def evalPrecedence(self, parser: Recognizer, outerContext: RuleContext) -> ta.Optional['SemanticContext']:
        return self


def andContext(a: SemanticContext, b: SemanticContext) -> SemanticContext:
    if a is None or a is SemanticContext.NONE:
        return b
    if b is None or b is SemanticContext.NONE:
        return a
    result = AND(a, b)
    if len(result.opnds) == 1:
        return result.opnds[0]
    else:
        return result


def orContext(a: SemanticContext, b: SemanticContext) -> SemanticContext:
    if a is None:
        return b
    if b is None:
        return a
    if a is SemanticContext.NONE or b is SemanticContext.NONE:
        return SemanticContext.NONE
    result = OR(a, b)
    if len(result.opnds) == 1:
        return result.opnds[0]
    else:
        return result


def filterPrecedencePredicates(collection: ta.AbstractSet[ta.Any]) -> ta.List['PrecedencePredicate']:
    return [context for context in collection if isinstance(context, PrecedencePredicate)]


class Predicate(SemanticContext):

    def __init__(self, ruleIndex: int = -1, predIndex: int = -1, isCtxDependent: bool = False) -> None:
        super().__init__()

        self.ruleIndex = ruleIndex
        self.predIndex = predIndex
        self.isCtxDependent = isCtxDependent

    def eval(self, parser: Recognizer, outerContext: RuleContext) -> bool:
        localctx = outerContext if self.isCtxDependent else None
        return parser.sempred(localctx, self.ruleIndex, self.predIndex)

    def __hash__(self) -> int:
        return hash((self.ruleIndex, self.predIndex, self.isCtxDependent))

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        elif not isinstance(other, Predicate):
            return False
        return (
                self.ruleIndex == other.ruleIndex and
                self.predIndex == other.predIndex and
                self.isCtxDependent == other.isCtxDependent
        )

    def __str__(self) -> str:
        return "{" + str(self.ruleIndex) + ":" + str(self.predIndex) + "}?"


class PrecedencePredicate(SemanticContext):

    def __init__(self, precedence: int = 0) -> None:
        super().__init__()

        self.precedence = precedence

    def eval(self, parser: Recognizer, outerContext: RuleContext) -> bool:
        return parser.precpred(outerContext, self.precedence)

    def evalPrecedence(self, parser: Recognizer, outerContext: RuleContext) -> ta.Optional[SemanticContext]:
        if parser.precpred(outerContext, self.precedence):
            return SemanticContext.NONE
        else:
            return None

    def __lt__(self, other: 'PrecedencePredicate') -> bool:
        return self.precedence < other.precedence

    def __hash__(self) -> int:
        return 31

    def __eq__(self, other: 'PrecedencePredicate') -> bool:
        if self is other:
            return True
        elif not isinstance(other, PrecedencePredicate):
            return False
        else:
            return self.precedence == other.precedence


class AND(SemanticContext):

    def __init__(self, a: SemanticContext, b: SemanticContext) -> None:
        super().__init__()

        operands = set()
        if isinstance(a, AND):
            operands.update(a.opnds)
        else:
            operands.add(a)
        if isinstance(b, AND):
            operands.update(b.opnds)
        else:
            operands.add(b)

        precedencePredicates = filterPrecedencePredicates(operands)
        if len(precedencePredicates) > 0:
            reduced = min(precedencePredicates)
            operands.add(reduced)

        self.opnds = list(operands)

    def __eq__(self, other: SemanticContext) -> bool:
        if self is other:
            return True
        elif not isinstance(other, AND):
            return False
        else:
            return self.opnds == other.opnds

    def __hash__(self) -> int:
        h = 0
        for o in self.opnds:
            h = hash((h, o))
        return hash((h, "AND"))

    def eval(self, parser: Recognizer, outerContext: RuleContext) -> bool:
        return all(opnd.eval(parser, outerContext) for opnd in self.opnds)

    def evalPrecedence(self, parser: Recognizer, outerContext: RuleContext) -> ta.Optional[SemanticContext]:
        differs = False
        operands = []
        for context in self.opnds:
            evaluated = context.evalPrecedence(parser, outerContext)
            differs |= evaluated is not context
            if evaluated is None:

                return None
            elif evaluated is not SemanticContext.NONE:

                operands.append(evaluated)

        if not differs:
            return self

        if len(operands) == 0:
            return SemanticContext.NONE

        result = None
        for o in operands:
            result = o if result is None else andContext(result, o)

        return result

    def __str__(self) -> str:
        with StringIO() as buf:
            first = True
            for o in self.opnds:
                if not first:
                    buf.write("&&")
                buf.write(str(o))
                first = False
            return buf.getvalue()


class OR(SemanticContext):

    def __init__(self, a: SemanticContext, b: SemanticContext) -> None:
        super().__init__()

        operands = set()
        if isinstance(a, OR):
            operands.update(a.opnds)
        else:
            operands.add(a)
        if isinstance(b, OR):
            operands.update(b.opnds)
        else:
            operands.add(b)

        precedencePredicates = filterPrecedencePredicates(operands)
        if len(precedencePredicates) > 0:
            s = sorted(precedencePredicates)
            reduced = s[-1]
            operands.add(reduced)

        self.opnds = list(operands)

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        elif not isinstance(other, OR):
            return False
        else:
            return self.opnds == other.opnds

    def __hash__(self) -> int:
        h = 0
        for o in self.opnds:
            h = hash((h, o))
        return hash((h, "OR"))

    def eval(self, parser: Recognizer, outerContext: RuleContext) -> bool:
        return any(opnd.eval(parser, outerContext) for opnd in self.opnds)

    def evalPrecedence(self, parser: Recognizer, outerContext: RuleContext) -> ta.Optional[SemanticContext]:
        differs = False
        operands = []
        for context in self.opnds:
            evaluated = context.evalPrecedence(parser, outerContext)
            differs |= evaluated is not context
            if evaluated is SemanticContext.NONE:
                return SemanticContext.NONE
            elif evaluated is not None:
                operands.append(evaluated)

        if not differs:
            return self

        if len(operands) == 0:
            return None

        result = None
        for o in operands:
            result = o if result is None else orContext(result, o)

        return result

    def __str__(self) -> str:
        with StringIO() as buf:
            first = True
            for o in self.opnds:
                if not first:
                    buf.write("||")
                buf.write(str(o))
                first = False
            return buf.getvalue()


SemanticContext.NONE = Predicate()


class PredictionContext:
    EMPTY = None

    EMPTY_RETURN_STATE = 0x7FFFFFFF

    globalNodeCount = 1
    id = globalNodeCount

    def __init__(self, cachedHashCode: int) -> None:
        super().__init__()

        self.cachedHashCode = cachedHashCode

    def __len__(self) -> int:
        return 0

    def isEmpty(self) -> bool:
        return self is self.EMPTY

    def hasEmptyPath(self) -> bool:
        return self.getReturnState(len(self) - 1) == self.EMPTY_RETURN_STATE

    def getReturnState(self, index: int) -> int:
        raise IllegalStateException("illegal!")

    def __hash__(self) -> int:
        return self.cachedHashCode


def calculateHashCode(parent: PredictionContext, returnState: int) -> int:
    return hash("") if parent is None else hash((hash(parent), returnState))


def calculateListsHashCode(parents: ta.Iterable[PredictionContext], returnStates: ta.Iterable[int]) -> int:
    h = 0
    for parent, returnState in zip(parents, returnStates):
        h = hash((h, calculateHashCode(parent, returnState)))
    return h


class PredictionContextCache:

    def __init__(self) -> None:
        super().__init__()

        self.cache = dict()

    def add(self, ctx: PredictionContext) -> PredictionContext:
        if ctx == PredictionContext.EMPTY:
            return PredictionContext.EMPTY
        existing = self.cache.get(ctx, None)
        if existing is not None:
            return existing
        self.cache[ctx] = ctx
        return ctx

    def get(self, ctx: PredictionContext) -> ta.Optional[PredictionContext]:
        return self.cache.get(ctx, None)

    def __len__(self):
        return len(self.cache)


class SingletonPredictionContext(PredictionContext):

    @staticmethod
    def create(parent: PredictionContext, returnState: int) -> 'SingletonPredictionContext':
        if returnState == PredictionContext.EMPTY_RETURN_STATE and parent is None:
            return SingletonPredictionContext.EMPTY
        else:
            return SingletonPredictionContext(parent, returnState)

    def __init__(self, parent: ta.Optional[PredictionContext], returnState: int) -> None:
        hashCode = calculateHashCode(parent, returnState)

        super().__init__(hashCode)

        self.parentCtx = parent
        self.returnState = returnState

    def __len__(self) -> int:
        return 1

    def getParent(self, index: int) -> PredictionContext:
        return self.parentCtx

    def getReturnState(self, index: int) -> int:
        return self.returnState

    def __eq__(self, other: 'SingletonPredictionContext') -> int:
        if self is other:
            return True
        elif other is None:
            return False
        elif not isinstance(other, SingletonPredictionContext):
            return False
        else:
            return self.returnState == other.returnState and self.parentCtx == other.parentCtx

    def __hash__(self) -> int:
        return self.cachedHashCode

    def __str__(self) -> str:
        up = "" if self.parentCtx is None else str(self.parentCtx)
        if len(up) == 0:
            if self.returnState == self.EMPTY_RETURN_STATE:
                return "$"
            else:
                return str(self.returnState)
        else:
            return str(self.returnState) + " " + up


class EmptyPredictionContext(SingletonPredictionContext):

    def __init__(self) -> None:
        super().__init__(None, self.EMPTY_RETURN_STATE)

    def isEmpty(self) -> bool:
        return True

    def __eq__(self, other: 'EmptyPredictionContext') -> bool:
        return self is other

    def __hash__(self) -> int:
        return self.cachedHashCode

    def __str__(self) -> str:
        return "$"


PredictionContext.EMPTY = EmptyPredictionContext()


class ArrayPredictionContext(PredictionContext):

    def __init__(self, parents: ta.List[PredictionContext], returnStates: ta.List[int]) -> None:
        super().__init__(calculateListsHashCode(parents, returnStates))

        self.parents = parents
        self.returnStates = returnStates

    def isEmpty(self) -> bool:
        return self.returnStates[0] == PredictionContext.EMPTY_RETURN_STATE

    def __len__(self) -> int:
        return len(self.returnStates)

    def getParent(self, index: int) -> PredictionContext:
        return self.parents[index]

    def getReturnState(self, index: int) -> int:
        return self.returnStates[index]

    def __eq__(self, other: 'ArrayPredictionContext') -> bool:
        if self is other:
            return True
        elif not isinstance(other, ArrayPredictionContext):
            return False
        elif hash(self) != hash(other):
            return False
        else:
            return self.returnStates == other.returnStates and self.parents == other.parents

    def __str__(self) -> str:
        if self.isEmpty():
            return "[]"
        with StringIO() as buf:
            buf.write("[")
            for i in range(0, len(self.returnStates)):
                if i > 0:
                    buf.write(", ")
                if self.returnStates[i] == PredictionContext.EMPTY_RETURN_STATE:
                    buf.write("$")
                    continue
                buf.write(str(self.returnStates[i]))
                if self.parents[i] is not None:
                    buf.write(' ')
                    buf.write(str(self.parents[i]))
                else:
                    buf.write("null")
            buf.write("]")
            return buf.getvalue()

    def __hash__(self) -> int:
        return self.cachedHashCode


def PredictionContextFromRuleContext(
        atn: ATN,
        outerContext: ta.Optional[RuleContext] = None,
) -> SingletonPredictionContext:
    if outerContext is None:
        outerContext = RuleContext.EMPTY

    if outerContext.parentCtx is None or outerContext is RuleContext.EMPTY:
        return PredictionContext.EMPTY

    parent = PredictionContextFromRuleContext(atn, outerContext.parentCtx)
    state = atn.states[outerContext.invokingState]
    transition = state.transitions[0]
    return SingletonPredictionContext.create(parent, transition.followState.stateNumber)


MergeCache = ta.Dict[ta.Tuple[PredictionContext, PredictionContext], PredictionContext]


def merge(
        a: PredictionContext,
        b: PredictionContext,
        rootIsWildcard: bool,
        mergeCache: MergeCache,
) -> PredictionContext:
    if a == b:
        return a

    if isinstance(a, SingletonPredictionContext) and isinstance(b, SingletonPredictionContext):
        return mergeSingletons(a, b, rootIsWildcard, mergeCache)

    if rootIsWildcard:
        if isinstance(a, EmptyPredictionContext):
            return a
        if isinstance(b, EmptyPredictionContext):
            return b

    if isinstance(a, SingletonPredictionContext):
        a = ArrayPredictionContext([a.parentCtx], [a.returnState])
    if isinstance(b, SingletonPredictionContext):
        b = ArrayPredictionContext([b.parentCtx], [b.returnState])
    return mergeArrays(a, b, rootIsWildcard, mergeCache)


def mergeSingletons(
        a: SingletonPredictionContext,
        b: SingletonPredictionContext,
        rootIsWildcard: bool,
        mergeCache: MergeCache,
) -> PredictionContext:
    if mergeCache is not None:
        previous = mergeCache.get((a, b), None)
        if previous is not None:
            return previous
        previous = mergeCache.get((b, a), None)
        if previous is not None:
            return previous

    merged = mergeRoot(a, b, rootIsWildcard)
    if merged is not None:
        if mergeCache is not None:
            mergeCache[(a, b)] = merged
        return merged

    if a.returnState == b.returnState:
        parent = merge(a.parentCtx, b.parentCtx, rootIsWildcard, mergeCache)

        if parent == a.parentCtx:
            return a
        if parent == b.parentCtx:
            return b

        merged = SingletonPredictionContext.create(parent, a.returnState)
        if mergeCache is not None:
            mergeCache[(a, b)] = merged
        return merged
    else:

        singleParent = None
        if a is b or (a.parentCtx is not None and a.parentCtx == b.parentCtx):
            singleParent = a.parentCtx
        if singleParent is not None:

            payloads = [a.returnState, b.returnState]
            if a.returnState > b.returnState:
                payloads = [b.returnState, a.returnState]
            parents = [singleParent, singleParent]
            merged = ArrayPredictionContext(parents, payloads)
            if mergeCache is not None:
                mergeCache[(a, b)] = merged
            return merged

        payloads = [a.returnState, b.returnState]
        parents = [a.parentCtx, b.parentCtx]
        if a.returnState > b.returnState:
            payloads = [b.returnState, a.returnState]
            parents = [b.parentCtx, a.parentCtx]
        merged = ArrayPredictionContext(parents, payloads)
        if mergeCache is not None:
            mergeCache[(a, b)] = merged
        return merged


def mergeRoot(
        a: SingletonPredictionContext,
        b: SingletonPredictionContext,
        rootIsWildcard: bool,
) -> ta.Optional[PredictionContext]:
    if rootIsWildcard:
        if a == PredictionContext.EMPTY:
            return PredictionContext.EMPTY
        if b == PredictionContext.EMPTY:
            return PredictionContext.EMPTY
    else:
        if a == PredictionContext.EMPTY and b == PredictionContext.EMPTY:
            return PredictionContext.EMPTY
        elif a == PredictionContext.EMPTY:
            payloads = [b.returnState, PredictionContext.EMPTY_RETURN_STATE]
            parents = [b.parentCtx, None]
            return ArrayPredictionContext(parents, payloads)
        elif b == PredictionContext.EMPTY:
            payloads = [a.returnState, PredictionContext.EMPTY_RETURN_STATE]
            parents = [a.parentCtx, None]
            return ArrayPredictionContext(parents, payloads)
    return None


def mergeArrays(
        a: ArrayPredictionContext,
        b: ArrayPredictionContext,
        rootIsWildcard: bool,
        mergeCache: MergeCache
) -> PredictionContext:
    if mergeCache is not None:
        previous = mergeCache.get((a, b), None)
        if previous is not None:
            return previous
        previous = mergeCache.get((b, a), None)
        if previous is not None:
            return previous

    i = 0
    j = 0
    k = 0

    mergedReturnStates = [None] * (len(a.returnStates) + len(b.returnStates))
    mergedParents = [None] * len(mergedReturnStates)

    while i < len(a.returnStates) and j < len(b.returnStates):
        a_parent = a.parents[i]
        b_parent = b.parents[j]
        if a.returnStates[i] == b.returnStates[j]:

            payload = a.returnStates[i]

            bothDollars = payload == PredictionContext.EMPTY_RETURN_STATE and a_parent is None and b_parent is None
            ax_ax = (a_parent is not None and b_parent is not None) and a_parent == b_parent
            if bothDollars or ax_ax:
                mergedParents[k] = a_parent
                mergedReturnStates[k] = payload
            else:
                mergedParent = merge(a_parent, b_parent, rootIsWildcard, mergeCache)
                mergedParents[k] = mergedParent
                mergedReturnStates[k] = payload
            i += 1
            j += 1
        elif a.returnStates[i] < b.returnStates[j]:
            mergedParents[k] = a_parent
            mergedReturnStates[k] = a.returnStates[i]
            i += 1
        else:
            mergedParents[k] = b_parent
            mergedReturnStates[k] = b.returnStates[j]
            j += 1
        k += 1

    if i < len(a.returnStates):
        for p in range(i, len(a.returnStates)):
            mergedParents[k] = a.parents[p]
            mergedReturnStates[k] = a.returnStates[p]
            k += 1
    else:
        for p in range(j, len(b.returnStates)):
            mergedParents[k] = b.parents[p]
            mergedReturnStates[k] = b.returnStates[p]
            k += 1

    if k < len(mergedParents):
        if k == 1:
            merged = SingletonPredictionContext.create(mergedParents[0], mergedReturnStates[0])
            if mergeCache is not None:
                mergeCache[(a, b)] = merged
            return merged
        mergedParents = mergedParents[0:k]
        mergedReturnStates = mergedReturnStates[0:k]

    merged = ArrayPredictionContext(mergedParents, mergedReturnStates)

    if merged == a:
        if mergeCache is not None:
            mergeCache[(a, b)] = a
        return a
    if merged == b:
        if mergeCache is not None:
            mergeCache[(a, b)] = b
        return b
    combineCommonParents(mergedParents)

    if mergeCache is not None:
        mergeCache[(a, b)] = merged
    return merged


def combineCommonParents(parents: list) -> None:
    uniqueParents = dict()

    for p in range(0, len(parents)):
        parent = parents[p]
        if uniqueParents.get(parent, None) is None:
            uniqueParents[parent] = parent

    for p in range(0, len(parents)):
        parents[p] = uniqueParents[parents[p]]


def getCachedPredictionContext(context: PredictionContext, contextCache: PredictionContextCache, visited: dict):
    if context.isEmpty():
        return context
    existing = visited.get(context)
    if existing is not None:
        return existing
    existing = contextCache.get(context)
    if existing is not None:
        visited[context] = existing
        return existing
    changed = False
    parents = [None] * len(context)
    for i in range(0, len(parents)):
        parent = getCachedPredictionContext(context.getParent(i), contextCache, visited)
        if changed or parent is not context.getParent(i):
            if not changed:
                parents = [context.getParent(j) for j in range(len(context))]
                changed = True
            parents[i] = parent
    if not changed:
        contextCache.add(context)
        visited[context] = context
        return context

    if len(parents) == 0:
        updated = PredictionContext.EMPTY
    elif len(parents) == 1:
        updated = SingletonPredictionContext.create(parents[0], context.getReturnState(0))
    else:
        updated = ArrayPredictionContext(parents, context.returnStates)

    contextCache.add(updated)
    visited[updated] = updated
    visited[context] = updated

    return updated


def getAllContextNodes(context: PredictionContext, nodes: ta.Optional[list] = None, visited: ta.Optional[dict] = None):
    if nodes is None:
        nodes = list()
        return getAllContextNodes(context, nodes, visited)
    elif visited is None:
        visited = dict()
        return getAllContextNodes(context, nodes, visited)
    else:
        if context is None or visited.get(context, None) is not None:
            return nodes
        visited.put(context, context)
        nodes.add(context)
        for i in range(0, len(context)):
            getAllContextNodes(context.getParent(i), nodes, visited)
        return nodes
