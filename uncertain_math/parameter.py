import numpy as np

from .number import Number


class Parameter(Number):
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
