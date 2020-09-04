from uncertain_math import Parameter, Sensor, uncertain
from uncertain_math.parameter import pretty_string


# Initialize our measurement device
digital_calipers = Sensor(resolution=0.1)
# Create a length parameter to measure length
length = Parameter(t_estimator=1.812)
# Create a width parameter to measure width
# Note: .like(length) will make it use the same t_estimator as length
width = Parameter.like(length)

# Take some readings:
# Note: `length &= ...` can be read as "length also equals..."
length &= digital_calipers.reading(11.1)
length &= digital_calipers.reading(11.3)
# length &= digital_calipers.reading(11.0)

width &= digital_calipers.reading(5.4)
width &= digital_calipers.reading(5.6)
# width &= digital_calipers.reading(5.5)

print(length)
print(width)
print(length > width)

# Now use the parameters to compute area
# Note: putting `@uncertain` above the function name tells the code that we
#       want to know both the mean and the uncertainty
@uncertain
def area(l, w):
    return l * w

print(area(length, width))
print(pretty_string(*area(length, width)))
