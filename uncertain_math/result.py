from .number import Number


class Result(Number):
    def __init__(self, mean, uncertainty):
        self._mean = mean
        self._uncertainty = uncertainty

    @property
    def mean(self):
        return self._mean

    @property
    def uncertainty(self):
        return self._uncertainty
