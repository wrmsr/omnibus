# type: ignore
#
# Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root.
# /
from functools import reduce
from io import StringIO
import typing as ta

from .._vendor.antlr4.atn.ATN import ATN
from .._vendor.antlr4.atn.ATNSimulator import ATNSimulator
from .._vendor.antlr4.atn.ATNState import ATNState
from .._vendor.antlr4.atn.ATNState import DecisionState
from .._vendor.antlr4.atn.ATNState import RuleStopState
from .._vendor.antlr4.atn.LexerActionExecutor import LexerActionExecutor
from .._vendor.antlr4.atn.SemanticContext import SemanticContext
from .._vendor.antlr4.atn.Transition import Transition
from .._vendor.antlr4.dfa.DFAState import DFAState
from .._vendor.antlr4.error.Errors import IllegalStateException
from .._vendor.antlr4.error.Errors import LexerNoViableAltException
from .._vendor.antlr4.error.Errors import UnsupportedOperationException
from .._vendor.antlr4.InputStream import InputStream
from .._vendor.antlr4.Lexer import Lexer
from .._vendor.antlr4.PredictionContext import merge
from .._vendor.antlr4.PredictionContext import PredictionContext
from .._vendor.antlr4.PredictionContext import PredictionContextCache
from .._vendor.antlr4.PredictionContext import SingletonPredictionContext
from .._vendor.antlr4.Token import Token
from .._vendor.antlr4.Utils import str_list


class SimState:

    def __init__(self):
        self.reset()

    def reset(self):
        self.index = -1
        self.line = 0
        self.column = -1
        self.dfaState = None


class LexerATNSimulator(ATNSimulator):
    MIN_DFA_EDGE = 0
    MAX_DFA_EDGE = 127

    ERROR = None

    match_calls = 0

    def __init__(
            self,
            recog: Lexer,
            atn: ATN,
            decisionToDFA: list,
            sharedContextCache: PredictionContextCache,
    ):
        super().__init__(atn, sharedContextCache)
        self.decisionToDFA = decisionToDFA
        self.recog = recog
        self.startIndex = -1
        self.line = 1
        self.column = 0
        self.mode = Lexer.DEFAULT_MODE
        self.prevAccept = SimState()

    def copyState(self, simulator: 'LexerATNSimulator'):
        self.column = simulator.column
        self.line = simulator.line
        self.mode = simulator.mode
        self.startIndex = simulator.startIndex

    def match(self, input: InputStream, mode: int):
        self.match_calls += 1
        self.mode = mode
        mark = input.mark()
        try:
            self.startIndex = input.index
            self.prevAccept.reset()
            dfa = self.decisionToDFA[mode]
            if dfa.s0 is None:
                return self.matchATN(input)
            else:
                return self.execATN(input, dfa.s0)
        finally:
            input.release(mark)

    def reset(self):
        self.prevAccept.reset()
        self.startIndex = -1
        self.line = 1
        self.column = 0
        self.mode = Lexer.DEFAULT_MODE

    def matchATN(self, input: InputStream):
        startState = self.atn.modeToStartState[self.mode]

        s0_closure = self.computeStartState(input, startState)
        suppressEdge = s0_closure.hasSemanticContext
        s0_closure.hasSemanticContext = False

        next = self.addDFAState(s0_closure)
        if not suppressEdge:
            self.decisionToDFA[self.mode].s0 = next

        predict = self.execATN(input, next)

        return predict

    def execATN(self, input: InputStream, ds0: DFAState):
        if ds0.isAcceptState:
            self.captureSimState(self.prevAccept, input, ds0)

        t = input.LA(1)
        s = ds0

        while True:
            target = self.getExistingTargetState(s, t)
            if target is None:
                target = self.computeTargetState(input, s, t)

            if target == self.ERROR:
                break

            if t != Token.EOF:
                self.consume(input)

            if target.isAcceptState:
                self.captureSimState(self.prevAccept, input, target)
                if t == Token.EOF:
                    break

            t = input.LA(1)

            s = target

        return self.failOrAccept(self.prevAccept, input, s.configs, t)

    def getExistingTargetState(self, s: DFAState, t: int):
        if s.edges is None or t < self.MIN_DFA_EDGE or t > self.MAX_DFA_EDGE:
            return None

        target = s.edges[t - self.MIN_DFA_EDGE]
        return target

    def computeTargetState(self, input: InputStream, s: DFAState, t: int):
        reach = ATNConfigSet()

        self.getReachableConfigSet(input, s.configs, reach, t)

        if len(reach) == 0:
            if not reach.hasSemanticContext:
                self.addDFAEdge(s, t, self.ERROR)

            return self.ERROR

        return self.addDFAEdge(s, t, cfgs=reach)

    def failOrAccept(self, prevAccept: SimState, input: InputStream, reach: 'ATNConfigSet', t: int):
        if self.prevAccept.dfaState is not None:
            lexerActionExecutor = prevAccept.dfaState.lexerActionExecutor
            self.accept(
                input,
                lexerActionExecutor,
                self.startIndex,
                prevAccept.index,
                prevAccept.line,
                prevAccept.column,
            )
            return prevAccept.dfaState.prediction
        else:
            if t == Token.EOF and input.index == self.startIndex:
                return Token.EOF
            raise LexerNoViableAltException(self.recog, input, self.startIndex, reach)

    def getReachableConfigSet(self, input: InputStream, closure: 'ATNConfigSet', reach: 'ATNConfigSet', t: int):
        skipAlt = ATN.INVALID_ALT_NUMBER
        for cfg in closure:
            currentAltReachedAcceptState = (cfg.alt == skipAlt)
            if currentAltReachedAcceptState and cfg.passedThroughNonGreedyDecision:
                continue

            for trans in cfg.state.transitions:
                target = self.getReachableTarget(trans, t)
                if target is not None:
                    lexerActionExecutor = cfg.lexerActionExecutor
                    if lexerActionExecutor is not None:
                        lexerActionExecutor = lexerActionExecutor.fixOffsetBeforeMatch(input.index - self.startIndex)

                    treatEofAsEpsilon = (t == Token.EOF)
                    config = LexerATNConfig(state=target, lexerActionExecutor=lexerActionExecutor, config=cfg)
                    if self.closure(input, config, reach, currentAltReachedAcceptState, True, treatEofAsEpsilon):
                        skipAlt = cfg.alt

    def accept(
            self,
            input: InputStream,
            lexerActionExecutor: LexerActionExecutor,
            startIndex: int,
            index: int,
            line: int,
            charPos: int,
    ):
        input.seek(index)
        self.line = line
        self.column = charPos

        if lexerActionExecutor is not None and self.recog is not None:
            lexerActionExecutor.execute(self.recog, input, startIndex)

    def getReachableTarget(self, trans: Transition, t: int):
        if trans.matches(t, 0, Lexer.MAX_CHAR_VALUE):
            return trans.target
        else:
            return None

    def computeStartState(self, input: InputStream, p: ATNState):
        initialContext = PredictionContext.EMPTY
        configs = ATNConfigSet()
        for i in range(0, len(p.transitions)):
            target = p.transitions[i].target
            c = LexerATNConfig(state=target, alt=i + 1, context=initialContext)
            self.closure(input, c, configs, False, False, False)
        return configs

    def closure(
            self,
            input: InputStream,
            config: 'LexerATNConfig',
            configs: 'ATNConfigSet',
            currentAltReachedAcceptState: bool,
            speculative: bool,
            treatEofAsEpsilon: bool,
    ):
        if isinstance(config.state, RuleStopState):
            if config.context is None or config.context.hasEmptyPath():
                if config.context is None or config.context.isEmpty():
                    configs.add(config)
                    return True
                else:
                    configs.add(LexerATNConfig(state=config.state, config=config, context=PredictionContext.EMPTY))
                    currentAltReachedAcceptState = True

            if config.context is not None and not config.context.isEmpty():
                for i in range(0, len(config.context)):
                    if config.context.getReturnState(i) != PredictionContext.EMPTY_RETURN_STATE:
                        newContext = config.context.getParent(i)
                        returnState = self.atn.states[config.context.getReturnState(i)]
                        c = LexerATNConfig(state=returnState, config=config, context=newContext)
                        currentAltReachedAcceptState = self.closure(
                            input,
                            c,
                            configs,
                            currentAltReachedAcceptState,
                            speculative,
                            treatEofAsEpsilon,
                        )

            return currentAltReachedAcceptState

        if not config.state.epsilonOnlyTransitions:
            if not currentAltReachedAcceptState or not config.passedThroughNonGreedyDecision:
                configs.add(config)

        for t in config.state.transitions:
            c = self.getEpsilonTarget(input, config, t, configs, speculative, treatEofAsEpsilon)
            if c is not None:
                currentAltReachedAcceptState = self.closure(
                    input,
                    c,
                    configs,
                    currentAltReachedAcceptState,
                    speculative,
                    treatEofAsEpsilon,
                )

        return currentAltReachedAcceptState

    def getEpsilonTarget(
            self,
            input: InputStream,
            config: 'LexerATNConfig',
            t: Transition,
            configs: 'ATNConfigSet',
            speculative: bool,
            treatEofAsEpsilon: bool,
    ):
        c = None
        if t.serializationType == Transition.RULE:
            newContext = SingletonPredictionContext.create(config.context, t.followState.stateNumber)
            c = LexerATNConfig(state=t.target, config=config, context=newContext)

        elif t.serializationType == Transition.PRECEDENCE:
            raise UnsupportedOperationException("Precedence predicates are not supported in lexers.")

        elif t.serializationType == Transition.PREDICATE:
            configs.hasSemanticContext = True
            if self.evaluatePredicate(input, t.ruleIndex, t.predIndex, speculative):
                c = LexerATNConfig(state=t.target, config=config)

        elif t.serializationType == Transition.ACTION:
            if config.context is None or config.context.hasEmptyPath():
                lexerActionExecutor = LexerActionExecutor.append(
                    config.lexerActionExecutor, self.atn.lexerActions[t.actionIndex])
                c = LexerATNConfig(state=t.target, config=config, lexerActionExecutor=lexerActionExecutor)

            else:
                c = LexerATNConfig(state=t.target, config=config)

        elif t.serializationType == Transition.EPSILON:
            c = LexerATNConfig(state=t.target, config=config)

        elif t.serializationType in [Transition.ATOM, Transition.RANGE, Transition.SET]:
            if treatEofAsEpsilon:
                if t.matches(Token.EOF, 0, Lexer.MAX_CHAR_VALUE):
                    c = LexerATNConfig(state=t.target, config=config)

        return c

    def evaluatePredicate(self, input: InputStream, ruleIndex: int, predIndex: int, speculative: bool):
        if self.recog is None:
            return True

        if not speculative:
            return self.recog.sempred(None, ruleIndex, predIndex)

        savedcolumn = self.column
        savedLine = self.line
        index = input.index
        marker = input.mark()
        try:
            self.consume(input)
            return self.recog.sempred(None, ruleIndex, predIndex)
        finally:
            self.column = savedcolumn
            self.line = savedLine
            input.seek(index)
            input.release(marker)

    def captureSimState(self, settings: SimState, input: InputStream, dfaState: DFAState):
        settings.index = input.index
        settings.line = self.line
        settings.column = self.column
        settings.dfaState = dfaState

    def addDFAEdge(self, from_: DFAState, tk: int, to: DFAState = None, cfgs: 'ATNConfigSet' = None) -> DFAState:

        if to is None and cfgs is not None:
            suppressEdge = cfgs.hasSemanticContext
            cfgs.hasSemanticContext = False

            to = self.addDFAState(cfgs)

            if suppressEdge:
                return to

        if tk < self.MIN_DFA_EDGE or tk > self.MAX_DFA_EDGE:
            return to

        if from_.edges is None:
            from_.edges = [None] * (self.MAX_DFA_EDGE - self.MIN_DFA_EDGE + 1)

        from_.edges[tk - self.MIN_DFA_EDGE] = to

        return to

    def addDFAState(self, configs: 'ATNConfigSet') -> DFAState:

        proposed = DFAState(configs=configs)
        firstConfigWithRuleStopState = next((cfg for cfg in configs if isinstance(cfg.state, RuleStopState)), None)

        if firstConfigWithRuleStopState is not None:
            proposed.isAcceptState = True
            proposed.lexerActionExecutor = firstConfigWithRuleStopState.lexerActionExecutor
            proposed.prediction = self.atn.ruleToTokenType[firstConfigWithRuleStopState.state.ruleIndex]

        dfa = self.decisionToDFA[self.mode]
        existing = dfa.states.get(proposed, None)
        if existing is not None:
            return existing

        newState = proposed

        newState.stateNumber = len(dfa.states)
        configs.setReadonly(True)
        newState.configs = configs
        dfa.states[newState] = newState
        return newState

    def getDFA(self, mode: int):
        return self.decisionToDFA[mode]

    def getText(self, input: InputStream):
        return input.getText(self.startIndex, input.index - 1)

    def consume(self, input: InputStream):
        curChar = input.LA(1)
        if curChar == ord('\n'):
            self.line += 1
            self.column = 0
        else:
            self.column += 1
        input.consume()

    def getTokenName(self, t: int):
        if t == -1:
            return "EOF"
        else:
            return "'" + chr(t) + "'"


class ATNConfig:

    def __init__(
            self,
            state: ATNState = None,
            alt: int = None,
            context: PredictionContext = None,
            semantic: SemanticContext = None,
            config: 'ATNConfig' = None,
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
        elif not isinstance(other, ATNConfig):
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

    def hashCodeForConfigSet(self):
        return hash((self.state.stateNumber, self.alt, hash(self.semanticContext)))

    def equalsForConfigSet(self, other):
        if self is other:
            return True
        elif not isinstance(other, ATNConfig):
            return False
        else:
            return self.state.stateNumber == other.state.stateNumber \
                   and self.alt == other.alt \
                   and self.semanticContext == other.semanticContext

    def __str__(self):
        with StringIO() as buf:
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


class LexerATNConfig(ATNConfig):

    def __init__(
            self,
            state: ATNState,
            alt: int = None,
            context: PredictionContext = None,
            semantic: SemanticContext = SemanticContext.NONE,
            lexerActionExecutor: LexerActionExecutor = None,
            config: 'LexerATNConfig' = None,
    ):
        super().__init__(state=state, alt=alt, context=context, semantic=semantic, config=config)
        if config is not None:
            if lexerActionExecutor is None:
                lexerActionExecutor = config.lexerActionExecutor
        self.lexerActionExecutor = lexerActionExecutor
        self.passedThroughNonGreedyDecision = False if config is None else self.checkNonGreedyDecision(config, state)

    def __hash__(self):
        return hash((
            self.state.stateNumber,
            self.alt,
            self.context,
            self.semanticContext,
            self.passedThroughNonGreedyDecision,
            self.lexerActionExecutor
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
        return super().__eq__(other)

    def hashCodeForConfigSet(self):
        return hash(self)

    def equalsForConfigSet(self, other):
        return self == other

    def checkNonGreedyDecision(self, source: 'LexerATNConfig', target: ATNState):
        return source.passedThroughNonGreedyDecision or isinstance(target, DecisionState) and target.nonGreedy


class ATNConfigSet:

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
            self.configs.append(config)  # track order here
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
        self.configLookup = None

    def __str__(self):
        with StringIO() as buf:
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


LexerATNSimulator.ERROR = DFAState(0x7FFFFFFF, ATNConfigSet())
