import operator
import tempfile
import textwrap
import typing as ta

from .. import local as local_
from ... import lang
from ... import properties
from ...dev.testing.helpers import skip_if_cant_import

if ta.TYPE_CHECKING:
    import pyspark as ps
else:
    ps = lang.proxy_import('pyspark')


class Driver:

    DEFAULT_CONFIGS = {
        'spark.speculation': 'false',
    }

    @properties.cached
    def session(self) -> 'ps.sql.SparkSession':
        ssb = ps.sql.SparkSession.builder
        ssb.appName('spark_virtualenv')
        for k, v in self.DEFAULT_CONFIGS.items():
            ssb.config(k, v)
        ssb.config('spark.sql.warehouse.dir', tempfile.mkdtemp())
        ss = ssb.getOrCreate()

        sc = ss.sparkContext
        log4j = sc._jvm.org.apache.log4j
        log4j.LogManager.getRootLogger().setLevel(log4j.Level.ERROR)

        return ss

    @properties.cached
    def context(self) -> 'ps.context.SparkContext':
        return self.session.sparkContext

    def drive(self):
        try:
            data = self.context.parallelize(list("Hello World"))
            counts = data \
                .map(lambda x: (x, 1)) \
                .reduceByKey(operator.add) \
                .sortBy(lambda x: x[1], ascending=False) \
                .collect()
            for word, count in counts:
                print("{}: {}".format(word, count))

        finally:
            self.context.stop()


@skip_if_cant_import('pyspark')
def test_local_launcher():
    launcher = local_.LocalLauncher(textwrap.dedent(f"""
    from {__name__} import Driver
    Driver().drive()
    """))
    launcher.launch()
