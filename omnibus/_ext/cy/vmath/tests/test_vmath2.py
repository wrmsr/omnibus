import array

from .. import vmath2 as vm2  # type: ignore


def test_add():
    t = 'f'
    l = 10
    a1 = array.array(t, [0.] * l)
    a2 = array.array(t, list(map(float, range(l))))
    a3 = array.array(t, list(map(float, range(l, l * 2))))
    vm2.op(vm2._pfn_op_add_sz_pf32_pf32_pf32, [('sz', l), ('pf32', a1), ('pf32', a2), ('pf32', a3)])
    assert list(a1) == [l + r for l, r in zip(a2, a3)]
