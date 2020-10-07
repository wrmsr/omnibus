import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import typing as ta

from .. import properties
from .. import pydevd
from ..jvm.jdk import find_java_home


class LocalLauncher:

    def __init__(
            self,
            code: str,
            args: ta.Sequence[str] = None,
            env: ta.Optional[ta.Mapping[str, str]] = None,
            *,
            jvm_debug_port: ta.Optional[int] = None,
            jvm_debug_suspend: ta.Optional[bool] = False,
    ) -> None:
        super().__init__()

        self._code = code
        self._args = args
        self._env = env

        self._jvm_debug_port = jvm_debug_port
        self._jvm_debug_suspend = jvm_debug_suspend

    @properties.cached
    def submit_path(self) -> str:
        submit_path = os.path.join(os.path.dirname(sys.executable), 'spark-submit')
        if not os.path.exists(submit_path):
            submit_path = shutil.which('spark-submit')
        if not os.path.exists(submit_path):
            raise EnvironmentError('Cannot find spark-submit')
        return submit_path

    OSX_PLATFORM = 'darwin'
    OSX_JDK_PATH = '/Library/Java/JavaVirtualMachines'

    @properties.cached
    def java_home(self) -> ta.Optional[str]:
        return find_java_home()

    @properties.cached
    def submit_env(self) -> ta.Dict[str, str]:
        env = dict(os.environ)
        env['PATH'] = f'{os.path.dirname(sys.executable)}:{env.get("PATH")}'
        if 'SPARK_HOME' not in env:
            env['SPARK_HOME'] = os.path.dirname(importlib.util.find_spec('pyspark').origin)
        if 'JAVA_HOME' not in env and self.java_home:
            env['JAVA_HOME'] = self.java_home
        if self._env is not None:
            env.update(self._env)
        return env

    @properties.cached
    def bootstrap_path(self) -> str:
        tmpdir = tempfile.mkdtemp()
        bootstrap_path = os.path.join(tmpdir, 'bootstrap.py')
        with open(bootstrap_path, 'w') as f:
            f.write(textwrap.dedent(f"""
            import sys
            old_paths = set(sys.path)
            for new_path in {sys.path!r}:
                if new_path not in old_paths:
                    sys.path.insert(0, new_path)

            from {__package__.split(".")[0]} import pydevd
            pydevd.maybe_reexec(file=__file__, silence=True)
            """))
            f.write(self._code)
        return bootstrap_path

    @properties.cached
    def internal_env(self) -> ta.Mapping[str, str]:
        bin_path = os.path.dirname(sys.executable)
        proc = subprocess.Popen([
            '/bin/bash',
            '-c',
            f'cd {bin_path} && . ./load-spark-env.sh && env | sort',
        ], stdout=subprocess.PIPE)
        out, _ = proc.communicate()
        return {
            k: v
            for line in out.decode('utf-8').split('\n')
            if line
            for k, _, v in [line.strip().partition('=')]
            if k not in os.environ
        }

    def launch(self) -> None:
        if pydevd.is_running():
            pydevd.save_args()

        args = [
            '--master', 'local',
            '--conf', f'spark.python.daemon.module={__name__.rpartition(".")[0]}._daemon',
            *(self._args or []),
        ]

        if self._jvm_debug_port is not None:
            parts = [
                'transport=dt_socket',
                'server=y',
                f'suspend={"y" if self._jvm_debug_suspend else "n"}',
                f'address={self._jvm_debug_port}',
            ]
            args.extend([
                '--driver-java-options', f'-agentlib:jdwp={",".join(parts)}',
            ])

        proc = subprocess.Popen([
            self.submit_path,
            *args,
            self.bootstrap_path,
        ], env=self.submit_env)
        proc.communicate()
