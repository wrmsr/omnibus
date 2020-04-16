"""
todo:
 - create table paths(path varchar(1024); - norm, dedupe, index, etc (bonus points for 32bit key)
 - store lineno from stacktrace

http://www.logilab.org/856
http://www.python.org/dev/peps/pep-0302/

start / end / cumulative / exclusive time / vm_rss / vm_size
"""
import dataclasses as dc
import inspect
import logging
import os
import sys
import threading
import time
import types
import typing as ta


log = logging.getLogger(__name__)


@dc.dataclass(frozen=True)
class Stats:
    time: float
    vm_rss: int = 0
    vm_size: int = 0


class StatsFactory:

    def __init__(self, *, start_time: float = None) -> None:
        super().__init__()

        self._start_time = start_time if start_time is not None else time.time()

    def __call__(self) -> Stats:
        return Stats(
            time=time.time() - self._start_time,
        )

    PROC_MEM_KEYS_BY_FIELD = {
        'vm_size': 'VmSize',
        'vm_rss': 'VmRSS',
    }

    PROC_MEM_SCALE = {
        'kb': 1024.0,
        'mb': 1024.0 * 1024.0,
    }

    @classmethod
    def get_proc_status(cls) -> ta.Mapping[str, ta.Any]:
        with open('/proc/self/status', 'r') as status_file:
            status_block = status_file.read()

        status_fields = {
            field: value.strip()
            for line in status_block.split('\n')
            for field, _, value in [line.partition(':')]
        }

        status = {}

        for key, field in cls.PROC_MEM_KEYS_BY_FIELD.iteritems():
            num, unit = status_fields[field].split()

            status[key] = int(float(num) * cls.PROC_MEM_SCALE[unit.lower()])

        return status


StackTrace = ta.Sequence[str]


@dc.dataclass()
class Node:
    import_name: str = None
    import_fromlist: ta.Iterable[str] = None
    import_level: int = None

    pid: int = None
    tid: int = None

    stack_trace: StackTrace = None
    exception: Exception = None

    children: ta.List['Node'] = dc.field(default_factory=list)

    cached_id: int = None

    loaded_name: str = None
    loaded_file: str = None
    loaded_id: int = None

    start_stats: Stats = None
    exclusive_stats: Stats = None
    cumulative_stats: Stats = None
    end_stats: Stats = None

    seq: int = None
    depth: int = 0


class ImportTracer:

    def __init__(self) -> None:
        super().__init__()

        self._stats_factory = StatsFactory()

    def trace(self, root_module: str) -> Node:
        node_stack = [Node()]

        def new_import(name, globals=None, locals=None, fromlist=(), level=0):
            node = Node(
                import_name=name,
                import_fromlist=fromlist,
                import_level=level,
                pid=os.getpid(),
                tid=threading.current_thread().ident,
                stack_trace=[s[1:] for s in inspect.stack() if s[0].f_code.co_filename != __file__],
                cached_id=id(sys.modules[name]) if name in sys.modules else None,
                start_stats=self._stats_factory(),
            )

            node_stack[-1].children.append(node)
            node_stack.append(node)

            try:
                loaded = old_import(name, globals, locals, fromlist, level)
                if not isinstance(loaded, types.ModuleType):
                    raise TypeError(loaded)
                node.loaded_name = loaded.__name__
                node.loaded_id = id(loaded)
                node.loaded_file = getattr(loaded, '__file__', None)
                return loaded

            except Exception as ex:
                node.exception = ex
                raise

            finally:
                node.end_stats = self._stats_factory()
                if node_stack.pop() is not node:
                    raise RuntimeError(node_stack)

        old_import = __builtins__.__import__
        __builtins__.__import__ = new_import
        try:
            try:
                __import__(root_module, globals(), locals(), [], 0)
            except Exception:
                log.exception(f'root_module: {root_module}')
        finally:
             __builtins__.__import__ = old_import

        if len(node_stack) != 1 or len(node_stack[0].children) != 1:
            raise RuntimeError(node_stack)

        node = node_stack[0].children[0]
        fixup_node(node)
        return node


def fixup_node(node: Node, *, depth: int = 0, seq: int = 0) -> int:
    node.depth = depth
    node.seq = seq

    # agg_keys = ['time', 'vm_rss', 'vm_size']
    # for key in agg_keys:
    #     node['cumulative_' + key] = node['end_' + key] - node['start_' + key]
    #     node['exclusive_' + key] = node['cumulative_' + key]

    for child in node.children:
        seq = fixup_node(child, depth=depth + 1, seq=seq + 1)

        # for key in agg_keys:
        #     node['exclusive_' + key] -= child['cumulative_' + key]

    return seq


def main():
    _, mod = sys.argv
    node = ImportTracer().trace(mod)
    import pprint
    pprint.pprint(dc.asdict(node))


if __name__ == '__main__':
    main()
