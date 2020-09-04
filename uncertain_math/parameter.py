import math

import numpy as np


def pretty_string(mean, uncertainty):
    decimals = -math.floor(math.log(uncertainty, 10))
    mean = round(mean, decimals)
    uncertainty = round(uncertainty, decimals)
    # noinspection PyStringFormat
    return f'{{:.{decimals}f}} +/- {{:.{decimals}}}'.format(mean, uncertainty)


class Parameter:
    def __init__(self, t_estimator=1.0):
        self.t_estimator = t_estimator
        self.measurements = []

    @classmethod
    def like(cls, other):
        return cls(t_estimator=other.t_estimator)

    def __iand__(self, measurement):
        self.measurements.append(measurement)
        return self

    @property
    def mean(self):
        assert len(self.measurements) > 0, 'Take some measurements first!'
        return np.mean(np.array(self.measurements)[:, 0])

    @property
    def uncertainty(self):
        assert len(self.measurements) > 0, 'Take some measurements first!'
        measurements = np.array(self.measurements)
        # If multiple sensors of differing resolutions were used to get
        # the measurements, the worst sensor's resolution is used here
        resolution = np.max(measurements[:, 1])
        std_t = np.std(measurements[:, 0]) * self.t_estimator
        mean = np.mean(measurements[:, 0])
        precision = np.max(np.abs(mean - measurements[:, 0]))

        return max(resolution, std_t, precision)

    @property
    def relative_uncertainty(self):
        return self.uncertainty / self.mean

    def __str__(self):
        return pretty_string(self.mean, self.uncertainty)

    def __eq__(self, other):
        s = self.mean
        s_u = self.uncertainty
        o = other.mean
        o_u = other.uncertainty
        return (s - s_u < o + o_u < s + s_u) or (o - o_u < s + s_u < o + o_u)

    def __lt__(self, other):
        return self.mean + self.uncertainty < other.mean - other.uncertainty

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return self.mean - self.uncertainty > other.mean + other.uncertainty

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
