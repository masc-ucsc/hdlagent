# PyRTL Hardware Description Language Documentation

PyRTL provides a Python-based environment for designing and simulating hardware. It offers a unique approach to hardware design, allowing for rapid prototyping and testing. Below is a concise guide to help language models like me generate PyRTL code effectively.

## Basic Concepts

### Wires and Logic
- **Wires** are the fundamental building blocks, connecting logic elements.
- **Logic** is created by combining wires using operators (e.g., `+`, `-`, `&`, `|`, `^`).
- Special wire types include **Input**, **Output**, **Const**, and **Register**.

### WireVector
- Main class for describing connections.
- Supports various operations like addition, subtraction, bitwise operations, and slicing.
- Example: `result = a + b` creates an adder.

### Registers
- Sequential elements that hold a value across clock cycles.
- Created by subclassing `WireVector`.
- Example: `reg = pyrtl.Register(bitwidth=8)`

## Input and Output Pins
- **Input** pins are placeholders for external values.
- **Output** pins represent the final output of a design.
- Example: `inp = pyrtl.Input(bitwidth=8)`

## Constants
- Represent hard-wired values.
- Example: `const_val = pyrtl.Const(5, bitwidth=3)`

## Conditional Assignment
- Allows for conditional logic within hardware design.
- Utilizes `with` blocks for defining conditions.
- Example:
  ```python
  with pyrtl.conditional_assignment:
      with condition:
          reg.next |= value
  ```

## Logic Nets and Blocks
- **LogicNets** represent primitive operations (e.g., add, subtract, and, or).
- **Blocks** encapsulate a netlist, defining the hardware's logic structure.

## Helper Functions

### Concatenation and Bit Manipulation
- `pyrtl.concat()` and `pyrtl.concat_list()` for combining WireVectors.
- `pyrtl.match_bitwidth()` for matching the bitwidth of WireVectors.

### Conversion and Interpretation
- `pyrtl.val_to_signed_integer()` for interpreting values as signed integers.
- `pyrtl.val_to_formatted_str()` and `pyrtl.formatted_str_to_val()` for converting between values and human-readable strings.

## Debugging
- `pyrtl.set_debug_mode()` to enable/disable debug mode.
- `pyrtl.probe()` for printing information about a WireVector.
- `pyrtl.rtl_assert()` for adding hardware assertions.

## Reductions
- Functions like `pyrtl.and_all_bits()`, `pyrtl.or_all_bits()`, and `pyrtl.xor_all_bits()` for reducing WireVectors to single bits.

## Extended Logic and Arithmetic
- Functions for signed arithmetic (`pyrtl.signed_add()`, `pyrtl.signed_mult()`) and comparisons (`pyrtl.signed_lt()`, `pyrtl.signed_le()`, etc.).
- Shift operations (`pyrtl.shift_left_arithmetic()`, `pyrtl.shift_right_arithmetic()`, etc.).

## Registers and Memories
- **Registers** hold values across clock cycles.
- **MemBlock** for read-write memories, supporting indexing for read and write operations.
- **RomBlock** for read-only memories, initialized with predefined data.

This documentation provides a foundation for understanding and generating PyRTL code. By leveraging these concepts and functions, one can design and simulate complex hardware systems within a Python environment.
