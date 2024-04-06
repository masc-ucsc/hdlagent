# PyRTL Documentation Summary

PyRTL is a Python library for Register Transfer Level (RTL) design, allowing for the description, simulation, and synthesis of digital hardware. It provides a Pythonic way to describe hardware by treating wires and logic operations as first-class objects. Below is a summary of key concepts and functionalities in PyRTL, including code snippets and syntax.

## Wires and Logic

- **WireVector**: Main class for describing connections between operators. Supports operations like addition, subtraction, multiplication, bitwise operations, comparisons, and slicing.
  ```python
  a, b = pyrtl.Input(8), pyrtl.Input(8)
  result = a + b  # Addition
  ```

- **Input, Output, Const, Register**: Specialized WireVectors for inputs, outputs, constants, and registers.
  ```python
  i = pyrtl.Input(bitwidth=8, name='i')
  o = pyrtl.Output(bitwidth=8, name='o')
  const = pyrtl.Const(5, bitwidth=3)
  reg = pyrtl.Register(bitwidth=8, name='reg')
  ```

## Logic Nets and Blocks

- **LogicNet**: Immutable datatype for storing a "net" in a netlist, representing hardware logic operations.
- **Block**: Encapsulates a netlist, storing both the basic logic elements and the wires and memories connecting them.

## Conditional Assignments

- Allows for conditional assignment of registers and WireVectors based on a predicate.
  ```python
  with pyrtl.conditional_assignment:
      with a:
          r1.next |= i
  ```

## Memory

- **MemBlock**: Object for specifying block memories, supporting both reading and writing.
  ```python
  memory = pyrtl.MemBlock(bitwidth=32, addrwidth=5)
  data = memory[addr]
  memory[addr] <<= data
  ```

- **RomBlock**: Read-only memory block initialized with specific values.
  ```python
  rom = pyrtl.RomBlock(bitwidth=8, addrwidth=4, romdata=[1, 2, 3, 4])
  data = rom[addr]
  ```

## Helper Functions

- **probe**: Prints information about a WireVector for debugging.
  ```python
  probe(w, name='debug_probe')
  ```

- **rtl_assert**: Adds hardware assertions to check conditions during simulation.
  ```python
  rtl_assert(w == 1, AssertionError("w is not 1"))
  ```

- **input_list, output_list, register_list**: Functions for creating lists of Inputs, Outputs, or Registers.
  ```python
  inputs = pyrtl.input_list('a, b, c', bitwidth=8)
  ```

- **val_to_signed_integer, formatted_str_to_val**: Functions for interpreting and converting values to and from signed integers and formatted strings.
  ```python
  signed_val = val_to_signed_integer(0xff, 8)
  val = formatted_str_to_val('101', 'b3')
  ```

## Arithmetic and Logic Extensions

- Provides functions for signed arithmetic, comparisons, and shifts.
  ```python
  result = pyrtl.signed_add(a, b)
  is_less = pyrtl.signed_lt(a, b)
  ```

This summary provides an overview of PyRTL's capabilities for describing and manipulating digital hardware designs in Python.
