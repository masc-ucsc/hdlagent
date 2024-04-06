**
\[WireVector\]**

**Description:**
A WireVector in PyRTL
 represents a set of wires that are treated like a logical unit.
It is
 the main class for describing the connections between operators.

**Example:**
```
>>> x = pyrtl.WireVector(8, 'x')

>>> y = pyrtl.WireVector(8, 'y')
>>> z = x + y
>>> assert z.bitwidth == 16

>>> assert len(z) == 16
>>> assert z.name == 'z'
```

**Properties:**
* `bitwidth`: The bitwidth of the wire vector.
* `name`: The name
 of the wire vector.
* `length`: The bitwidth of the wire vector.

**Methods:**
* `__add__(other)`: Adds two wire vectors together.
* `__sub__(other)`: Subtra
cts the right wire vector from the left one.
* `__mul__(other)`: Multiplies two wire vectors together.
* `__xor__(other)`: XORs two wire vectors together.
* `__or__(other)`: ORs two wire vectors together.
* `__and__(
other)`: ANDs two wire vectors together.
* `__invert__()`: Inverts the wire vector.
* `__lshift__(other)`: Left-shifts the wire vector by the given amount.
* `__rshift__(other)`: Right-shifts the wire vector by the given amount
.
* `__getitem__(slice)`: Selects a slice of the wire vector.
* `__setitem__(slice, value)`: Sets a slice of the wire vector to the given value.
* `__len__()`: Returns the length of the wire vector.
* `__str__()
`: Returns a string representation of the wire vector.
* `__repr__()`: Returns a string representation of the wire vector.
* `bitmask`: A bitmask of the same length as the wire vector, where each bit is set to 1.
* `bitwidth`: The bitwidth of the
 wire vector.
* `is_zero()`: Returns True if the wire vector is all zeros, False otherwise.
* `is_one()`: Returns True if the wire vector is all ones, False otherwise.
* `name`: The name of the wire vector.
* `operator_==`:
 Tests if the wire vector is equal to the given value.
* `operator_!=`: Tests if the wire vector is not equal to the given value.
* `operator_<`: Tests if the wire vector is less than the given value.
* `operator_<=`: Tests if the wire vector is less
 than or equal to the given value.
* `operator_>`: Tests if the wire vector is greater than the given value.
* `operator_>=`: Tests if the wire vector is greater than or equal to the given value.
