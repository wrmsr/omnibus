import gc
import weakref

dct = weakref.WeakKeyDictionary()
class C:
    pass
a = C()
b = C()
a.b = weakref.ref(b)
b.a = weakref.ref(a)
ar = weakref.ref(a)
br = weakref.ref(b)
dct[a] = b
del b
print(dct[a])
del a
print(list(dct.keys()))
import gc
gc.collect()
print(list(dct.keys()))
dct.clear()
print(ar())
gc.collect()
print(ar())
