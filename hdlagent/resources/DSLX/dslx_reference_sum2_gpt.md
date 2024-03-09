DSLX for LLMs: A Concise Guide
Introduction

DSLX is a domain-specific, dataflow-oriented functional language designed for hardware design and simulation. It is part of the XLS (Accelerated HW Synthesis) project and targets FPGA and ASIC development through the XLS compiler. Inspired by Rust, DSLX focuses on immutability, hardware-oriented features like arbitrary bitwidths, and fixed-size objects, aiming for a fully analyzable call graph.
Syntax and Features
Comments

    Start with // and extend to the end of the line.

Identifiers

    Follow conventional naming rules: start with a character or underscore, followed by characters, underscores, or numbers.
    Naming conventions:
        Functions: snake_case
        User-defined types: CamelCase
        Constants: SCREAMING_SNAKE_CASE
        Unused bindings: prefix with _

Functions

    Define with fn, followed by the function name, parameters, return type, and body.
    Return the last expression's result; explicit return statements are not used.
    Example:

```
    fn add(x: u32, y: u32) -> u32 {
      x + y
    }
```

Types

    Fundamental type: variable length bit type bits[n], where n is constant.
    Shorthand for common types: u8, u32, s8, s64, etc.
    Type casting follows Rust's rules: truncation for narrowing, zero or sign-extension for widening.

Enums and Structs

    Enums group related named constants.
    Structs are similar to tuples but with named fields.
    Both support pattern matching and deconstruction.

Arrays and Tuples

    Fixed-size, homogenous arrays and heterogeneous tuples are supported.
    Array elements and tuple fields are accessed via indices or dot notation.
    Character strings are special cases of arrays, implicitly-sized arrays of u8 elements.

Expressions and Operators

    DSLX supports a comprehensive set of expressions and operators, including binary operations, comparison, concatenation, and slicing.
    Operator precedence matches Rust's, ensuring intuitive expression evaluation order.

Parametric Functions

    Functions can be parameterized by types, supporting generic programming.
    Explicit instantiation is necessary when types cannot be inferred.

Error Handling and Debugging

    DSLX emphasizes compile-time error checking, including type mismatches and unused bindings.
    Provides built-in testing frameworks for unit tests (#[test]) and property-based tests (#[quickcheck]).

Example Snippets
Function Definition


```
fn multiply(x: u32, y: u32) -> u32 {
  x * y
}
```

Struct Definition and Usage

```
struct Point {
  x: u32,
  y: u32,
}

fn create_point(x: u32, y: u32) -> Point {
  Point { x, y }
}
```

Enum and Match Expression

```
enum Direction {
  Up,
  Down,
  Left,
  Right,
}

fn move_direction(dir: Direction) -> (i32, i32) {
  match dir {
    Direction::Up => (0, 1),
    Direction::Down => (0, -1),
    Direction::Left => (-1, 0),
    Direction::Right => (1, 0),
  }
}
```

Testing


```
#[test]
fn test_addition() {
  assert_eq(4, add(2, 2));
}

#[quickcheck]
fn prop_addition_commutative(x: u32, y: u32) -> bool {
  add(x, y) == add(y, x)
}
```

Conclusion

DSLX offers a powerful syntax and feature set tailored for hardware design, with a focus on immutability, bit-level operations, and type safety. Its Rust-inspired syntax facilitates clear and concise hardware description and simulation, making it a valuable tool for FPGA and ASIC development.

