from .sensor import Measurement, Sensor
from .parameter import Parameter

from jax import grad
import numpy as np


def uncertain(func):
    def inner(*args):
        mean_inputs = list(map(lambda x: x.mean, args))
        mean_output = func(*mean_inputs)

        partials = [grad(func, i) for i in range(len(args))]
        series = []
        for i, partial in enumerate(partials):
            series.append(args[i].uncertainty * partial(*mean_inputs))

        return mean_output.tolist(), np.linalg.norm(series)

    return inner
