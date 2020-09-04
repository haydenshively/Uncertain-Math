![Python package](https://github.com/haydenshively/Uncertain-Math/workflows/Python%20package/badge.svg)
# Uncertain-Math

An engineering toolkit for taking measurements and propagating uncertainty

## Introduction

With Uncertain Math, all you have to do is record your data. The code will automatically compute the mean & uncertainty
for every parameter. It also allows you to combine parameters to get results (e.g. combine `length`, `width`, and
`height` to get volume). It propagates the uncertainties through the calculation using `Jax`, a library normally used
for computing gradients for machine learning @ Google.

The example below shows what Uncertain Math can do. **If you want to jump right in and try things for yourself, check
out the [Collab Notebook](https://colab.research.google.com/drive/1w4AXHxYogSmrPAjFKG4gxiaKqIP55auH?usp=sharing) version
of this readme**

```python
digital_calipers = Sensor(resolution=0.1)

length = Parameter(t_estimator=1.812)
width = Parameter.like(length)

# Take some readings:
# Note: "length &=" can be read as "length also equals..."
length &= digital_calipers.reading(11.1)
length &= digital_calipers.reading(11.3)
length &= digital_calipers.reading(11.0)

width &= digital_calipers.reading(5.4)
width &= digital_calipers.reading(5.6)
width &= digital_calipers.reading(5.5)

# See the results immediately:
print(length) # prints: 11.1 +/- 0.2
print(width)  # prints: 5.5 +/- 0.1
print(length == width) # prints: False
print(length > width)  # prints: True

# Propagate uncertainty through a function:
@uncertain
def area(l, w):
    return l * w


print(area(length, width))
# prints: (61.233333333333334, 2.06353)
#          area_mean,          area_uncertainty
```

## How-to

### Create a sensor

`my_sensor = Sensor(resolution=0.1)`

Create a new sensor any time you're about to take measurements with a new device. The resolution of a digital measuring
device is the smallest place value on the display, while the resolution of an analog device is `0.5 * smallest_interval`.

`measurement = sensor.reading(1234.5)`

The `reading(value)` function returns a measurement. `measurement.value` spits out whatever value you put in, and
`measurement.resolution` will match the resolution of the sensor that took the reading. However, you probably won't want
to store `measurement` directly. Instead, immediately store the measurement in a parameter (see below).

### Define a parameter

`my_parameter = Parameter(t_estimator=3.1415)`

Create a new parameter when you're about to make measurements on a new dimension, voltage, resistance, etc. To store
measurements in your fancy new parameter:

```python
my_parameter &= my_sensor.reading(1234.5)
my_parameter &= my_sensor.reading(1235.4)
...
```

When finished adding measurements, simply call `print(my_parameter)` to see the mean and uncertainty. The code takes care
of `max(stddev, precision, resolution)` in the background. You can also compare parameters using built-in Python operators
(`==`, `>`, `<`, etc.) and it will take uncertainty into account.

### Propagate uncertainty

Let's say I define an ordinary Python function like the following:

```python
def volume(l, w, h):
  return l * w * h
```

To convert that into something that knows how to propagate uncertainty, all I have to do is stick an `@uncertain` above it:

```python
@uncertain
def volume(l, w, h):
  return l * w * h
```

As long as I've already defined parameters for length, width, and height (and stored measurements for them), I can just
pass those into the volume function and everything will just work:

```python
volume_mean, volume_uncertainty = volume(my_l_param, my_w_param, my_h_param)
```

*WARNING*: Right now, you can't chain these fancy uncertainty-understanding functions together. So if you want to subtract
two volumes, for example, you'll need to defined one large function that accepts all of the parameters
(`def volume(l1, w1, h1, l2, w2, h2)`) instead of two separate volumes that you subtract at the end. I plan to fix this
in the future.
