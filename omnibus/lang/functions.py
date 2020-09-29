import functools
import typing as ta


def typed_lambda(*ret, **kw):
    def inner(fn):
        ns = {}
        ns['__fn'] = fn
        proto = 'def __lam('
        call = 'return __fn('
        pkw = {k: v for k, v in kw.items() if k != 'return'}
        for i, (n, t) in enumerate(pkw.items()):
            if i:
                call += ', '
            else:
                proto += '*'
            ns['__ann_' + n] = t
            proto += f', {n}: __ann_{n}'
            call += f'{n}={n}'
        proto += ')'
        if 'return' in kw:
            ns['__ann_return'] = kw['return']
            proto += f' -> __ann_return'
        proto += ':'
        call += ')'
        src = f'{proto} {call}'
        exec(src, ns)
        return ns['__lam']
    if ret:
        [ret] = ret
        kw['return'] = ret
    for k in kw:
        if k.startswith('__'):
            raise NameError(k)
    return inner


def typed_partial(fn, **kw):
    for k in kw:
        if k.startswith('__'):
            raise NameError(k)
    th = ta.get_type_hints(fn)
    lam = typed_lambda(**{n: h for n, h in th.items() if n not in kw})(lambda **lkw: fn(**lkw, **kw))
    functools.update_wrapper(lam, fn, assigned=list(set(functools.WRAPPER_ASSIGNMENTS) - {'__annotations__'}))
    return lam
