**
Introduction**

PyRTL is a hardware description language designed to allow the user to
 describe hardware in the Python programming language. 

**Tutorial**

The tutorial
 starts by giving an example of a circuit defined in PyRTL, where the user provides an Adder:

```py 
from pyrtl import *
width
 = 32
a, b, sum = WireVector(width, 'a'), WireVector(width, 'b'), WireVector(width,
 's')
with conditional_assignment:
    with a < b:
        sum |= b - a
    with b < a:
        sum |= a - b
```

Then the tutorial introduces the concept of a
 PyRTL netlist and `LogicNet`, where the hardware described by the user is converted into logic gates. 

The tutorial then introduces blocks, which encapsulate the logic. A block stores a netlist and provides basic access and error
 checking members. Each block has well defined inputs and outputs, and contains both the basic logic elements and references to the wires and memories that connect them together.

The tutorial then discusses how to build a more complicated circuit that computes both add and subtract, where the user assigns `sum |= select(a, i, select
(c, k, default))`

**Summary**

The tutorial covers very basic aspects of PyRTL, including bitwise operations, conditionals, wirevector creation, and how to create a netlist and block.
