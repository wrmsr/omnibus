"""
Based on https://github.com/alecthomas/mph/
"""
import dataclasses as dc
import random
import typing as ta

from . import properties


uint16 = int
uint64 = int

MAX_UINT16 = 0xffff
MAX_UINT64 = 0xffffffffffffffff

_FNV_OFFSET = 0xcbf29ce484222325
_FNV_PRIME = 0x100000001b3

try:
    import pyhash

except ImportError:
    def fnv1a_64(data: bytes) -> uint64:
        hsh = _FNV_OFFSET
        for c in data:
            hsh ^= c
            hsh *= _FNV_PRIME
            hsh &= MAX_UINT64
        return hsh

else:
    fnv1a_64: ta.Callable[[bytes], uint64] = pyhash.fnv1a_64(_FNV_OFFSET)


@dc.dataclass()
class Bucket:
    index: uint64 = 0
    keys: ta.List[bytes] = dc.field(default_factory=list)
    values: ta.List[bytes] = dc.field(default_factory=list)


@dc.dataclass(frozen=True)
class Chd:
    r: ta.Sequence[uint64]
    indices: ta.Sequence[uint16]
    keys: ta.Sequence[bytes]
    values: ta.Sequence[bytes]

    def get(self, key: bytes) -> ta.Optional[bytes]:
        r0 = self.r[0]
        h = fnv1a_64(key) ^ r0
        i = h % len(self.indices)
        ri = self.indices[i]
        if ri >= len(self.r) & MAX_UINT16:
            # This can occur if there were unassigned slots in the hash table.
            return None
        r = self.r[ri]
        ti = (h ^ r) % len(self.keys)
        k = self.keys[ti]
        if k != key:
            return None
        v = self.values[ti]
        return v

    def len(self) -> int:
        return len(self.keys)


class ChdBuilder:

    def __init__(
            self,
            dct: ta.Mapping[bytes, bytes],
            *,
            rand_u64: ta.Callable[[], uint64] = None,
            max_iters: int = 10_000_000,
    ) -> None:
        super().__init__()

        self._dct = dct

        if rand_u64 is None:
            def rand_u64():
                return rand.randint(0, MAX_UINT64)
            rand = random.Random()

        self._rand_u64 = rand_u64
        self._max_iters = max_iters

        num_entries: uint64 = len(dct)
        num_buckets = num_entries // 2
        if num_buckets == 0:
            num_buckets = 1

        self._num_entries: uint64 = num_entries
        self._num_buckets: uint64 = num_buckets

        self._r: ta.List[uint64] = []
        self._add(rand_u64())

        self._keys: ta.List[bytes] = [None] * self._num_entries
        self._values: ta.List[bytes] = [None] * self._num_entries

        self._buckets: ta.List[Bucket] = [Bucket() for _ in range(self._num_buckets)]
        self._indices: ta.List[uint16] = [-1] * self._num_buckets

        self._seen: ta.Set[uint64] = set()

    def _add(self, r: uint64) -> None:
        self._r.append(r)

    def _table(self, r: uint64, b: bytes) -> uint64:
        return (fnv1a_64(b) ^ self._r[0] ^ r) % self._num_entries

    def _hash_index_from_key(self, b: bytes) -> uint64:
        return (fnv1a_64(b) ^ self._r[0]) % self._num_buckets

    def _try_hash(
            self,
            bucket: Bucket,
            ri: uint16,
            r: uint64
    ) -> bool:
        duplicates: ta.Set[uint64] = set()
        hashes: ta.List[uint64] = [0] * len(bucket.keys)

        for i, k in enumerate(bucket.keys):
            h = self._table(r, k)
            if h in self._seen or h in duplicates:
                return False
            duplicates.add(h)
            hashes[i] = h

        for h in hashes:
            self._seen.add(h)

        self._indices[bucket.index] = ri

        for i, h in enumerate(hashes):
            self._keys[h] = bucket.keys[i]
            self._values[h] = bucket.values[i]

        return True

    def _generate(self) -> ta.Tuple[uint16, uint64]:
        return (len(self._r), self._rand_u64())

    @properties.cached
    def chd(self) -> Chd:
        duplicates: ta.Set[bytes] = set()

        for key, value in self._dct.items():
            if key in duplicates:
                raise KeyError(key)
            duplicates.add(key)

            oh = self._hash_index_from_key(key)
            self._buckets[oh].index = oh
            self._buckets[oh].keys.append(key)
            self._buckets[oh].values.append(value)

        self._buckets.sort(key=lambda b: -len(b.keys))

        for i, bucket in enumerate(self._buckets):
            if not bucket.keys:
                continue

            cont = False
            for ri, r in enumerate(self._r):
                if self._try_hash(bucket, ri, r):
                    cont = True
                    break
            if cont:
                continue

            # Keep trying new functions until we get one that does not collide. The number of retries here is very high
            # to allow a very high probability of not getting collisions.
            for _ in range(self._max_iters):
                ri, r = self._generate()
                if self._try_hash(bucket, ri, r):
                    self._add(r)
                    cont = True
                    break
            if cont:
                continue

            raise RuntimeError(
                'Failed to find a collision-free hash function', i, len(self._buckets), len(bucket.keys), bucket)

        return Chd(
            self._r,
            self._indices,
            self._keys,
            self._values,
        )
