# PyRTL Documentation Summary

PyRTL is a Python library for designing and simulating hardware. It provides a Hardware Description Language (HDL) within Python, allowing for the description, simulation, and analysis of digital circuits. Below is a summary of key concepts and functionalities in PyRTL, including code snippets for clarity.

## Wires and Logic

- **Wires** are the basic building blocks in PyRTL, representing connections between logic blocks.
- **Logic** is created by combining wires using operators (e.g., `+`, `-`, `&`, `|`, `^`).
- **WireVector** is the main class for describing connections. It supports various operations like addition, subtraction, multiplication, bitwise operations, and comparisons.

### WireVector Example
```python
import pyrtl
a, b = pyrtl.Input(8, 'a'), pyrtl.Input(8, 'b')
result = a + b  # Creates an adder
```

## Input, Output, Const, and Register

- **Input** and **Output** represent external connections.
- **Const** is used for specifying constant values.
- **Register** represents sequential elements, updating on clock edges.

### Register Example
```python
reg = pyrtl.Register(bitwidth=8, name='reg')
reg.next <<= a + b  # Set next value of reg to be a + b
```

## Conditional Assignment

PyRTL supports conditional assignments using `with` blocks, allowing for hardware multiplexing and conditional logic.

### Conditional Assignment Example
```python
with pyrtl.conditional_assignment:
    with a:
        reg.next |= i
    with otherwise:
        reg.next |= j
```

## Logic Nets and Blocks

- **LogicNets** store the description of hardware logic operations.
- **Blocks** encapsulate a netlist, containing inputs, outputs, logic elements, and connections.

## Helper Functions

PyRTL provides various helper functions for tasks like concatenating WireVectors, matching bitwidths, and creating lists of WireVectors.

### Concatenation Example
```python
msb, lsb = pyrtl.Input(8, 'msb'), pyrtl.Input(8, 'lsb')
combined = pyrtl.concat(msb, lsb)  # Concatenates msb and lsb
```

## Debugging

PyRTL supports debugging through functions like `probe` and `rtl_assert`, which can be used to monitor signals and assert conditions during simulation.

### Probe Example
```python
pyrtl.probe(a, 'probe_a')  # Monitors the value of wire 'a'
```

## Memories and ROMs

PyRTL allows for the creation of read-write memories (`MemBlock`) and read-only memories (`RomBlock`), which can be indexed for reading and writing.

### Memory Example
```python
memory = pyrtl.MemBlock(bitwidth=32, addrwidth=10, name='memory')
data = memory[addr]  # Reading from memory
memory[addr] <<= data  # Writing to memory
```

## Arithmetic and Logic Extensions

PyRTL extends basic arithmetic and logic operations to support signed operations, shifts, and reductions.

### Signed Multiplication Example
```python
product = pyrtl.signed_mult(a, b)  # Multiplies a and b treating them as signed
```

This summary provides an overview of PyRTL's capabilities for hardware design and simulation within Python. For detailed usage and more advanced features, refer to the full PyRTL documentation.
