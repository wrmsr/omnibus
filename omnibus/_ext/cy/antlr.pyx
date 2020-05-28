from libcpp cimport bool

from functools import reduce
import io

from ..._vendor.antlr4 import InputStream
from ..._vendor.antlr4 import Lexer
from ..._vendor.antlr4 import LexerATNSimulator
from ..._vendor.antlr4 import Token
from ..._vendor.antlr4.atn.ATN import ATN
from ..._vendor.antlr4.atn.ATNConfig import ATNConfig
from ..._vendor.antlr4.atn.ATNConfig import LexerATNConfig
from ..._vendor.antlr4.atn.ATNConfigSet import ATNConfigSet
from ..._vendor.antlr4.atn.ATNSimulator import ATNSimulator
from ..._vendor.antlr4.atn.ATNState import ATNState
from ..._vendor.antlr4.atn.ATNState import DecisionState
from ..._vendor.antlr4.atn.ATNState import RuleStopState
from ..._vendor.antlr4.atn.LexerActionExecutor import LexerActionExecutor
from ..._vendor.antlr4.atn.SemanticContext import SemanticContext
from ..._vendor.antlr4.atn.Transition import Transition  # noqa
from ..._vendor.antlr4.error.Errors import IllegalStateException
from ..._vendor.antlr4.error.Errors import UnsupportedOperationException
from ..._vendor.antlr4.PredictionContext import merge
from ..._vendor.antlr4.PredictionContext import PredictionContext
from ..._vendor.antlr4.PredictionContext import SingletonPredictionContext
from ..._vendor.antlr4.Utils import str_list


DEF Transition__EPSILON     = 1
DEF Transition__RANGE       = 2
DEF Transition__RULE        = 3
DEF Transition__PREDICATE   = 4 # e.g., {isType(input.LT(1))}?
DEF Transition__ATOM        = 5
DEF Transition__ACTION      = 6
DEF Transition__SET         = 7 # ~(A|B) or ~atom, wildcard, which convert to next 2
DEF Transition__NOT_SET     = 8
DEF Transition__WILDCARD    = 9
DEF Transition__PRECEDENCE  = 10


for _check in [
    'not RuleStopState.__subclasses__()',
    f'{Transition__EPSILON}     == Transition.EPSILON',
    f'{Transition__RANGE}       == Transition.RANGE',
    f'{Transition__RULE}        == Transition.RULE',
    f'{Transition__PREDICATE}   == Transition.PREDICATE',
    f'{Transition__ATOM}        == Transition.ATOM',
    f'{Transition__ACTION}      == Transition.ACTION',
    f'{Transition__SET}         == Transition.SET',
    f'{Transition__NOT_SET}     == Transition.NOT_SET',
    f'{Transition__WILDCARD}    == Transition.WILDCARD',
    f'{Transition__PRECEDENCE}  == Transition.PRECEDENCE',
    'ATNConfig.__subclasses__() == [LexerATNConfig]',
    'not LexerATNConfig.__subclasses__()',
]:
    if not eval(_check):
        raise ImportError(_check)


cpdef bool LexerATNSimulator__closure(
        self: LexerATNSimulator,
        input: InputStream,
        config: LexerATNConfig,
        configs: ATNConfigSet,
        currentAltReachedAcceptState: bool,
        speculative: bool,
        treatEofAsEpsilon: bool
):
    if config.state.__class__ is RuleStopState:
        if config.context is None or config.context.hasEmptyPath():
            if config.context is None or config.context.isEmpty():
                configs.add(config)
                return True

            else:
                configs.add(LexerATNConfig(
                    state=config.state,
                    config=config,
                    context=PredictionContext.EMPTY,
                ))
                currentAltReachedAcceptState = True

        if config.context is not None and not config.context.isEmpty():
            for i in range(0, len(config.context)):
                if config.context.getReturnState(i) != PredictionContext.EMPTY_RETURN_STATE:
                    newContext = config.context.getParent(i)  # "pop" return state
                    returnState = self.atn.states[config.context.getReturnState(i)]

                    c = LexerATNConfig(
                        state=returnState,
                        config=config,
                        context=newContext,
                    )

                    currentAltReachedAcceptState = LexerATNSimulator__closure(
                        self,
                        input,
                        c,
                        configs,
                        currentAltReachedAcceptState,
                        speculative,
                        treatEofAsEpsilon,
                    )

        return currentAltReachedAcceptState

    # optimization
    if not config.state.epsilonOnlyTransitions:
        if not currentAltReachedAcceptState or not config.passedThroughNonGreedyDecision:
            configs.add(config)

    for t in config.state.transitions:
        c = None
        if t.serializationType == Transition__RULE:
            newContext = SingletonPredictionContext.create(config.context, t.followState.stateNumber)

            c = LexerATNConfig(
                state=t.target,
                config=config,
                context=newContext,
            )

        elif t.serializationType == Transition__PRECEDENCE:
            raise UnsupportedOperationException("Precedence predicates are not supported in lexers.")

        elif t.serializationType == Transition__PREDICATE:
            configs.hasSemanticContext = True
            if self.evaluatePredicate(input, t.ruleIndex, t.predIndex, speculative):
                c = LexerATNConfig(state=t.target, config=config)

        elif t.serializationType == Transition__ACTION:
            if config.context is None or config.context.hasEmptyPath():
                lexerActionExecutor = LexerActionExecutor.append(
                    config.lexerActionExecutor,
                    self.atn.lexerActions[t.actionIndex],
                )

                c = LexerATNConfig(
                    state=t.target,
                    config=config,
                    lexerActionExecutor=lexerActionExecutor,
                )

            else:
                # ignore actions in referenced rules
                c = LexerATNConfig(state=t.target, config=config)

        elif t.serializationType == Transition__EPSILON:
            c = LexerATNConfig(state=t.target, config=config)

        elif (
                t.serializationType == Transition__ATOM or
                t.serializationType == Transition__RANGE or
                t.serializationType == Transition__SET
        ):
            if treatEofAsEpsilon:
                if t.matches(Token.EOF, 0, Lexer.MAX_CHAR_VALUE):
                    c = LexerATNConfig(state=t.target, config=config)

        if c is not None:
            currentAltReachedAcceptState = LexerATNSimulator__closure(
                self,
                input,
                c,
                configs,
                currentAltReachedAcceptState,
                speculative,
                treatEofAsEpsilon,
            )

    return currentAltReachedAcceptState


cdef class CyATNConfig:

    cdef object state  # type: ATNStat
    cdef int alt

    cdef object context  # type: PredictionContext
    cdef object semantic  # type: SemanticContext

    cdef int reachesIntoOuterContext
    cdef bool precedenceFilterSuppressed

    def __init__(
            self,
            state: ATNState = None,
            alt: int = None,
            context: PredictionContext = None,
            semantic: SemanticContext = None,
            config: ATNConfig = None,
    ):
        if config is not None:
            if state is None:
                state = config.state
            if alt is None:
                alt = config.alt
            if context is None:
                context = config.context
            if semantic is None:
                semantic = config.semanticContext

        if semantic is None:
            semantic = SemanticContext.NONE

        self.state = state
        self.alt = alt

        self.context = context
        self.semanticContext = semantic

        self.reachesIntoOuterContext = 0 if config is None else config.reachesIntoOuterContext
        self.precedenceFilterSuppressed = False if config is None else config.precedenceFilterSuppressed

    def __eq__(self, other):
        if self is other:
            return True
        elif not isinstance(other, CyATNConfig):
            return False
        else:
            return (
                    self.state.stateNumber == other.state.stateNumber and
                    self.alt == other.alt and
                    ((self.context is other.context) or (self.context == other.context)) and
                    self.semanticContext == other.semanticContext and
                    self.precedenceFilterSuppressed == other.precedenceFilterSuppressed
            )

    def __hash__(self):
        return hash((self.state.stateNumber, self.alt, self.context, self.semanticContext))

    cpdef hashCodeForConfigSet(self):
        return hash((self.state.stateNumber, self.alt, hash(self.semanticContext)))

    cpdef equalsForConfigSet(self, other):
        if self is other:
            return True
        elif not isinstance(other, ATNConfig):
            return False
        else:
            return (
                    self.state.stateNumber == other.state.stateNumber and
                    self.alt == other.alt and
                    self.semanticContext == other.semanticContext
            )

    def __str__(self):
        with io.StringIO() as buf:
            buf.write('(')
            buf.write(str(self.state))
            buf.write(",")
            buf.write(str(self.alt))
            if self.context is not None:
                buf.write(",[")
                buf.write(str(self.context))
                buf.write("]")
            if self.semanticContext is not None and self.semanticContext is not SemanticContext.NONE:
                buf.write(",")
                buf.write(str(self.semanticContext))
            if self.reachesIntoOuterContext > 0:
                buf.write(",up=")
                buf.write(str(self.reachesIntoOuterContext))
            buf.write(')')
            return buf.getvalue()


cdef class CyLexerATNConfig(CyATNConfig):

    cdef object lexerActionExecutor  # type: LexerActionExecutor
    cdef bool passedThroughNonGreedyDecision

    def __init__(
            self,
            state: ATNState,
            alt: int = None,
            context: PredictionContext = None,
            semantic: SemanticContext = SemanticContext.NONE,
            lexerActionExecutor: LexerActionExecutor = None,
            config: LexerATNConfig = None,
    ):
        CyATNConfig.__init__(state=state, alt=alt, context=context, semantic=semantic, config=config)

        if config is not None:
            if lexerActionExecutor is None:
                lexerActionExecutor = config.lexerActionExecutor

        # This is the backing field for {@link #getLexerActionExecutor}.
        self.lexerActionExecutor = lexerActionExecutor
        self.passedThroughNonGreedyDecision = False if config is None else self.checkNonGreedyDecision(config, state)

    def __hash__(self):
        return hash((
            self.state.stateNumber,
            self.alt,
            self.context,
            self.semanticContext,
            self.passedThroughNonGreedyDecision,
            self.lexerActionExecutor,
        ))

    def __eq__(self, other):
        if self is other:
            return True
        elif not isinstance(other, LexerATNConfig):
            return False
        if self.passedThroughNonGreedyDecision != other.passedThroughNonGreedyDecision:
            return False
        if not (self.lexerActionExecutor == other.lexerActionExecutor):
            return False
        return CyATNConfig.__eq__(other)

    cpdef hashCodeForConfigSet(self):
        return hash(self)

    cpdef equalsForConfigSet(self, other):
        return self == other

    cpdef checkNonGreedyDecision(self, source: LexerATNConfig, target: ATNState):
        return source.passedThroughNonGreedyDecision or isinstance(target, DecisionState) and target.nonGreedy


cdef class CyATNConfigSet:

    def __init__(self, fullCtx: bool = True):
        self.configLookup = dict()
        self.fullCtx = fullCtx
        self.readonly = False
        self.configs = []

        self.uniqueAlt = 0
        self.conflictingAlts = None

        self.hasSemanticContext = False
        self.dipsIntoOuterContext = False

        self.cachedHashCode = -1

    def __iter__(self):
        return self.configs.__iter__()

    def add(self, config: ATNConfig, mergeCache=None):
        if self.readonly:
            raise Exception("This set is readonly")

        if config.semanticContext is not SemanticContext.NONE:
            self.hasSemanticContext = True

        if config.reachesIntoOuterContext > 0:
            self.dipsIntoOuterContext = True

        existing = self.getOrAdd(config)
        if existing is config:
            self.cachedHashCode = -1
            self.configs.append(config)
            return True

        rootIsWildcard = not self.fullCtx
        merged = merge(existing.context, config.context, rootIsWildcard, mergeCache)

        existing.reachesIntoOuterContext = max(existing.reachesIntoOuterContext, config.reachesIntoOuterContext)

        if config.precedenceFilterSuppressed:
            existing.precedenceFilterSuppressed = True

        existing.context = merged

        return True

    def getOrAdd(self, config: ATNConfig):
        h = config.hashCodeForConfigSet()
        l = self.configLookup.get(h, None)
        if l is not None:
            r = next((cfg for cfg in l if config.equalsForConfigSet(cfg)), None)
            if r is not None:
                return r
        if l is None:
            l = [config]
            self.configLookup[h] = l
        else:
            l.append(config)
        return config

    def getStates(self):
        return set(c.state for c in self.configs)

    def getPredicates(self):
        return list(cfg.semanticContext for cfg in self.configs if cfg.semanticContext != SemanticContext.NONE)

    def get(self, i: int):
        return self.configs[i]

    def optimizeConfigs(self, interpreter: ATNSimulator):
        if self.readonly:
            raise IllegalStateException("This set is readonly")
        if len(self.configs) == 0:
            return
        for config in self.configs:
            config.context = interpreter.getCachedContext(config.context)

    def addAll(self, coll: list):
        for c in coll:
            self.add(c)
        return False

    def __eq__(self, other):
        if self is other:
            return True
        elif not isinstance(other, ATNConfigSet):
            return False

        same = (
                self.configs is not None and
                self.configs == other.configs and
                self.fullCtx == other.fullCtx and
                self.uniqueAlt == other.uniqueAlt and
                self.conflictingAlts == other.conflictingAlts and
                self.hasSemanticContext == other.hasSemanticContext and
                self.dipsIntoOuterContext == other.dipsIntoOuterContext
        )

        return same

    def __hash__(self):
        if self.readonly:
            if self.cachedHashCode == -1:
                self.cachedHashCode = self.hashConfigs()
            return self.cachedHashCode
        return self.hashConfigs()

    def hashConfigs(self):
        return reduce(lambda h, cfg: hash((h, cfg)), self.configs, 0)

    def __len__(self):
        return len(self.configs)

    def isEmpty(self):
        return len(self.configs) == 0

    def __contains__(self, config):
        if self.configLookup is None:
            raise UnsupportedOperationException("This method is not implemented for readonly sets.")
        h = config.hashCodeForConfigSet()
        l = self.configLookup.get(h, None)
        if l is not None:
            for c in l:
                if config.equalsForConfigSet(c):
                    return True
        return False

    def clear(self):
        if self.readonly:
            raise IllegalStateException("This set is readonly")
        self.configs.clear()
        self.cachedHashCode = -1
        self.configLookup.clear()

    def setReadonly(self, readonly: bool):
        self.readonly = readonly
        self.configLookup = None  # can't mod, no need for lookup cache

    def __str__(self):
        with io.StringIO() as buf:
            buf.write(str_list(self.configs))
            if self.hasSemanticContext:
                buf.write(",hasSemanticContext=")
                buf.write(str(self.hasSemanticContext))
            if self.uniqueAlt != ATN.INVALID_ALT_NUMBER:
                buf.write(",uniqueAlt=")
                buf.write(str(self.uniqueAlt))
            if self.conflictingAlts is not None:
                buf.write(",conflictingAlts=")
                buf.write(str(self.conflictingAlts))
            if self.dipsIntoOuterContext:
                buf.write(",dipsIntoOuterContext")
            return buf.getvalue()


cdef class CyOrderedATNConfigSet(CyATNConfigSet):

    def __init__(self):
        super().__init__()
