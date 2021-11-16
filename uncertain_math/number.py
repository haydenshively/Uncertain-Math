import abc
import math


def pretty_string(mean, uncertainty):
    decimals = -math.floor(math.log(uncertainty, 10))
    mean = round(mean, decimals)
    uncertainty = round(uncertainty, decimals)
    decimals = max(decimals, 0)
    # noinspection PyStringFormat
    return f'{{:.{decimals}f}} +/- {{:.{decimals}f}}'.format(mean, uncertainty)


class Number(abc.ABC):
    @property
    @abc.abstractmethod
    def mean(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def uncertainty(self):
        raise NotImplementedError

    @property
    def relative_uncertainty(self):
        return self.uncertainty / self.mean

    @property
    def max(self):
        return self.mean + self.uncertainty

    @property
    def min(self):
        return self.mean - self.uncertainty

    def __str__(self):
        return pretty_string(self.mean, self.uncertainty)

    def __eq__(self, other):
        s = self
        o = other
        return (s.min < o.max < s.max) or (o.min < s.max < o.max)

    def __lt__(self, other):
        return self.max < other.min

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return self.min > other.max

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
