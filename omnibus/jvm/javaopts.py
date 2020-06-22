"""
https://chriswhocodes.com/hotspot_options_jdk14.html
http://www.oracle.com/technetwork/java/javase/tech/vmoptions-jsp-140102.html
http://www.oracle.com/technetwork/java/javase/tech/exactoptions-jsp-141536.html

http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/tip/src/share/vm/runtime/arguments.cpp
http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/tip/src/share/vm/runtime/arguments.hpp
http://hg.openjdk.java.net/jdk8/jdk8/hotspot/file/tip/src/share/vm/runtime/globals.hpp

-Djava.security.egd=file:/dev/./urandom
-Dsun.net.inetaddr.ttl=0
java.security.Security.setProperty("networkaddress.cache.ttl" , "60");

-XX:BCEATraceLevel=3
-XX:MaxBCEAEstimateSize=1024
-XX:MaxInlineSize=256
-XX:FreqInlineSize=1024
-XX:MaxInlineLevel=22
-XX:CompileThreshold=10
"""
import abc
import enum
import typing as ta

from .. import dataclasses as dc
from .. import defs


T = ta.TypeVar('T')


class Prefix(enum.Enum):
    NONE = ''
    DASH = '-'
    NONSTANDARD = '-X'
    UNSTABLE = '-XX:'
    PROPERTY = '-D'


class Separator(enum.Enum):
    NONE = ''
    COLON = ':'
    EQUALS = '='


class Item(ta.Generic[T]):

    def __init__(self, prefix: Prefix, name: str, separator: Separator) -> None:
        super().__init__()

        self._prefix = prefix
        self._name = name
        self._separator = separator

    defs.basic('prefix', 'name', 'separator')

    @property
    def prefix(self) -> Prefix:
        return self._prefix

    @property
    def name(self) -> str:
        return self._name

    @property
    def separator(self) -> Separator:
        return self._separator

    @abc.abstractmethod
    def __call__(self, rendered: str) -> str:
        return self.prefix.value + self.name + self.separator.value + rendered


class ValuelessItem(Item[None]):

    def __init__(self, prefix: Prefix, name: str) -> None:
        super().__init__(prefix, name, Separator.NONE)

    def __call__(self) -> str:
        return super().__call__('')


class StringItem(Item[str]):

    def __call__(self, value: str) -> str:
        return super().__call__(value)


class IntItem(Item[int]):

    def __call__(self, value: int) -> str:
        return super().__call__(str(value))


class DataSizeEntry(dc.Pure):
    num_bytes: int
    suffix: str


class DataSize(enum.Enum):
    B = DataSizeEntry(1, '')
    KB = DataSizeEntry(1 << 10, 'k')
    MB = DataSizeEntry(1 << 20, 'm')
    GB = DataSizeEntry(1 << 30, 'g')


class DataSizeItem(Item[DataSize]):

    def __call__(self, value: int, unit: DataSize) -> str:
        return super().__call__(str(value) + unit.value.suffix)


class ToggleItem(Item[bool]):

    def __init__(self, prefix: Prefix, name: str) -> None:
        super().__init__(prefix, name, Separator.NONE)

    def __call__(self, value: bool) -> str:
        return self.prefix.value + ('+' if value else '-') + self.name


class ValuelessPropertyItem(ValuelessItem):

    def __init__(self, name: str) -> None:
        super().__init__(Prefix.PROPERTY, name)


class FixedItem(StringItem):

    def __init__(self, prefix: Prefix, name: str, separator: Separator, value: str) -> None:
        super().__init__(prefix, name, separator)

        self._value = value

    defs.basic('prefix', 'name', 'separator', 'value')

    @property
    def value(self) -> str:
        return self._value

    def __call__(self) -> str:
        return super().__call__(self.value)


class PropertyItem(StringItem):

    def __init__(self, name: str) -> None:
        super().__init__(Prefix.PROPERTY, name, Separator.EQUALS)


class BooleanPropertyItem(Item[bool]):

    def __init__(self, name: str) -> None:
        super().__init__(Prefix.PROPERTY, name, Separator.EQUALS)

    def __call__(self, value: bool) -> str:
        return super().__call__('true' if value else 'false')


class IntPropertyItem(Item[int]):

    def __init__(self, name: str) -> None:
        super().__init__(Prefix.PROPERTY, name, Separator.EQUALS)

    def __call__(self, value: int) -> str:
        return super().__call__(str(value))


MIN_HEAP_SIZE = DataSizeItem(Prefix.NONSTANDARD, 'ms', Separator.NONE)
MAX_HEAP_SIZE = DataSizeItem(Prefix.NONSTANDARD, 'mx', Separator.NONE)

YOUNG_GENERATION_SIZE = DataSizeItem(Prefix.NONSTANDARD, 'mn', Separator.NONE)
THREAD_STACK_SIZE = DataSizeItem(Prefix.NONSTANDARD, 'ss', Separator.NONE)
MAX_DIRECT_MEMORY_SIZE = DataSizeItem(Prefix.UNSTABLE, 'MaxDirectMemorySize', Separator.EQUALS)

PRINT_GC_DATE_STAMPS = ToggleItem(Prefix.UNSTABLE, 'PrintGCDateStamps')
PRINT_GC_DETAILS = ToggleItem(Prefix.UNSTABLE, 'PrintGCDetails')
PRINT_TENURING_DISTRIBUTION = ToggleItem(Prefix.UNSTABLE, 'PrintTenuringDistribution')
PRINT_JNI_GC_STALLS = ToggleItem(Prefix.UNSTABLE, 'PrintJNIGCStalls')
PRINT_GC_APPLICATION_STOPPED_TIME = ToggleItem(Prefix.UNSTABLE, 'PrintGCApplicationStoppedTime')
LOG_GC = StringItem(Prefix.NONSTANDARD, 'loggc', Separator.COLON)

VERBOSE_CLASS = FixedItem(Prefix.DASH, 'verbose', Separator.COLON, 'class')
VERBOSE_GC = FixedItem(Prefix.DASH, 'verbose', Separator.COLON, 'gc')
VERBOSE_JNI = FixedItem(Prefix.DASH, 'verbose', Separator.COLON, 'jni')

CHECK_JNI = FixedItem(Prefix.DASH, 'check', Separator.COLON, 'jni')

USE_NUMA = ToggleItem(Prefix.UNSTABLE, 'UseNUMA')

HEAP_DUMP_ON_OUT_OF_MEMORY_ERROR = ToggleItem(Prefix.UNSTABLE, 'HeapDumpOnOutOfMemoryError')
HEAP_DUMP_PATH = StringItem(Prefix.UNSTABLE, 'HeapDumpPath', Separator.EQUALS)

SERVER = ValuelessItem(Prefix.DASH, 'server')
MIXED = ValuelessItem(Prefix.NONSTANDARD, 'mixed')
FUTURE = ValuelessItem(Prefix.NONSTANDARD, 'future')
PROF = ValuelessItem(Prefix.NONSTANDARD, 'prof')
BATCH = ValuelessItem(Prefix.NONSTANDARD, 'batch')

INTERPRETED = ValuelessItem(Prefix.NONSTANDARD, 'int')

BIASED_LOCKING_rightUP_DELAY = IntItem(Prefix.UNSTABLE, 'BiasedLockingStartupDelay', Separator.EQUALS)
ABORT_VM_ON_EXCEPTION = StringItem(Prefix.UNSTABLE, 'AbortVMOnException', Separator.EQUALS)

ON_OUT_OF_MEMORY_ERROR = StringItem(Prefix.UNSTABLE, 'OnOutOfMemoryError', Separator.EQUALS)
ON_ERROR = StringItem(Prefix.UNSTABLE, 'OnError', Separator.EQUALS)

PRINT_FLAGS_FINAL = ToggleItem(Prefix.UNSTABLE, 'PrintFlagsFinal')

UNLOCK_DIAGNOSTIC_VM_OPTIONS = ToggleItem(Prefix.UNSTABLE, 'UnlockDiagnosticVMOptions')
ELIMINATE_LOCKS = ToggleItem(Prefix.UNSTABLE, 'EliminateLocks')
USE_LARGE_PAGES = ToggleItem(Prefix.UNSTABLE, 'UseLargePages')
UNLOCK_EXPERIMENTAL_VM_OPTIONS = ToggleItem(Prefix.UNSTABLE, 'UnlockExperimentalVMOptions')
USE_JVMCI_COMPILER = ToggleItem(Prefix.UNSTABLE, 'UseJVMCICompiler')

DEBUG = ValuelessItem(Prefix.NONSTANDARD, 'debug')

PRINT_INLINING = ToggleItem(Prefix.UNSTABLE, 'PrintInlining')
PRINT_COMPILATION = ToggleItem(Prefix.UNSTABLE, 'PrintCompilation')
PRINT_CLASS_HISTOGRAM = ToggleItem(Prefix.UNSTABLE, 'PrintClassHistogram')

USE_COMPRESSED_OOPS = ToggleItem(Prefix.UNSTABLE, 'UseCompressedOops')

OBJECT_ALIGNMENT_IN_BYTES = StringItem(Prefix.UNSTABLE, 'ObjectAlignmentInBytes', Separator.EQUALS)

ALWAYS_PRE_TOUCH = ToggleItem(Prefix.UNSTABLE, 'AlwaysPreTouch')


class RemoteDebugItem(StringItem):

    def __init__(self) -> None:
        super().__init__(Prefix.NONSTANDARD, 'runjdwp', Separator.COLON)

    def __call__(self, port: int, suspend: bool) -> str:
        return super().__call__(f"transport=dt_socket,address={port},server=y,suspend={'y' if suspend else 'n'}")


REMOTE_DEBUG = RemoteDebugItem()


HEADLESS = BooleanPropertyItem('java.awt.headless')

JMX_REMOTE = ValuelessPropertyItem('com.sun.management.jmxremote')
JMX_REMOTE_PORT = PropertyItem('com.sun.management.jmxremote.port')
JMX_REMOTE_LOCAL_ONLY = PropertyItem('com.sun.management.jmxremote.local.only')
JMX_REMOTE_AUTHENTICATE = PropertyItem('com.sun.management.jmxremote.authenticate')
JMX_REMOTE_SSL = PropertyItem('com.sun.management.jmxremote.ssl')

PREFER_IPV4_STACK = BooleanPropertyItem('java.net.preferIPv4Stack')
INET_ADDR_TTL = IntPropertyItem('sun.net.inetaddr.ttl')
