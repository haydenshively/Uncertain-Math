from collections import namedtuple


Measurement = namedtuple('Measurement', ['value', 'resolution'])


class Sensor:
    def __init__(self, resolution):
        self.resolution = resolution

    def reading(self, value):
        return Measurement(value, self.resolution)
