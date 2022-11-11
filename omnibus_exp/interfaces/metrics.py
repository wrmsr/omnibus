import abc

from .. import lang


class MetricsCollection(lang.Abstract):
    """
    https://github.com/statsd/statsd/blob/master/docs/metric_types.md
    https://docs.datadoghq.com/api/?lang=bash#api-reference
    """

    @abc.abstractmethod
    def gauge(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def count(self, name: str, num: int = 1) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def timing(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, name: str) -> None:
        raise NotImplementedError


class NopMetricsCollection(MetricsCollection):

    def gauge(self, name: str) -> None:
        pass

    def count(self, name: str, num: int = 1) -> None:
        pass

    def timing(self, name: str) -> None:
        pass

    def set(self, name: str) -> None:
        pass


class PrefixedMetricsCollection(MetricsCollection):

    def gauge(self, name: str) -> None:
        raise TypeError

    def count(self, name: str, num: int = 1) -> None:
        raise TypeError

    def timing(self, name: str) -> None:
        raise TypeError

    def set(self, name: str) -> None:
        raise TypeError


class CompositeMetricsCollection(MetricsCollection):

    def gauge(self, name: str) -> None:
        raise TypeError

    def count(self, name: str, num: int = 1) -> None:
        raise TypeError

    def timing(self, name: str) -> None:
        raise TypeError

    def set(self, name: str) -> None:
        raise TypeError
