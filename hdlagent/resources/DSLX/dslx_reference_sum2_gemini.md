## DSLX Reference: Types, Functions, Expressions, and More

### Overview

DSLX is a domain specific, dataflow-oriented functional language that compiles to
the XLS hardware description language. DSLX offers automatic hardware generation
via conversion to XLS IR, which can be passed to downstream XLS core
functionality (e.g. compilation to FPGA/ASIC).

### Comments

Comments in DSLX start with `//` and last through the end of the line.

### Identifiers

Identifiers in DSLX follow the typical naming rules of other languages, but
recommend adherence to the Rust naming conventions. Valid characters include
lowercase, uppercase, digits, and underscore, and must start with a character or
underscore. Invalid examples would be `_0` and `&ade`.

### Functions

Functions in DSLX begin with the keyword `fn`, followed by the function name, a
parameter list in parenthesis, an `->` and the return type of the function. The
function body is wrapped in curly braces.

Simple examples:

```dslx
fn ret3() -> u32 {
  u32:3  // This function always returns 3.
}

fn add1(x: u32) -> u32 {
  x + u32:1 // Returns x + 1, but you knew that!
}
```

Functions return the result of the last computed expression as their return
value. There are no explicit return statements. Functions must have a single return
value.

Tuples should be returned to return multiple values.

### Parameters

Parameters are written as pairs of `<name>` followed by a colon `:` followed by
the `<type>` of that parameter. Each parameter needs to declare its own type.

Examples:

```
// a simple parameter x of type u32
  x: u32

// t is a tuple with 2 elements.
//  the 1st element is of type u32
//  the 2nd element is a tuple with 3 elements
//      the 1st element is of type u8
//      the 2nd element is another tuple with 1 element of type u16
//      the 3rd element is of type u8
  t: (u32, (u8, (u16,), u8))
```

### Parametric Functions

DSLX functions can be parameterized in terms of the types of its arguments and in
terms of types derived from other parametric values. For instance:

```dslx
fn double(n: u32) -> u32 {
 n * u32:2
}

fn self_append<A: u32, B: u32 = {double(A)}>(lhs: bits[A]) -> bits[B] {
 lhs++lhs
}

fn main() -> bits[10] {
 self_append(u5:1)
}
```

In `self_append(bits[5]:1)`, we see that `A = 5` based off of formal argument
instantiation. Using that value, we can evaluate `B = double(A=5)`. This derived
expression is analogous to C++'s constexpr – a simple expression that can be
evaluated at that point in compilation. Note that the expression must be wrapped
in `{}` curly braces.

### Types

DSLX introduces aliases for commonly used types, such as `u8` for an 8-wide bit
type, or `u32` for a 32-bit wide bit type. These are defined up to `u64`.

All `u*`, `uN[*]`, and `bits[*]` types are interpreted as unsigned integers.
Signed integers are specified via `s*` and `sN[*]`. Similarly to unsigned
numbers, the `s*` shorthands are defined up to `s64`.

#### Bit Type Attributes

Bit types have helpful type-level attributes that provide limit values, similar
to `std::numeric_limits` in C++. For example:

```dslx
u3::MAX  // u3:0b111 the "fill with ones" value
s3::MAX  // s3:0b011 the "maximum signed" value

u3::ZERO // u3:0b000 the "fill with zeros" value
s3::ZERO // s3:0b000 the "fill with zeros" value
```

### Enum Types

Enums are a way of defining a group of related, scoped, named constants that do
not pollute the module namespace. For example:

```dslx
enum Opcode : u3 {
 FIRE_THE_MISSILES = 0,
 BE_TIRED = 1,
 TAKE_A_NAP = 2,
}
```

Casting of enum-values works with the same casting/extension rules that apply to the
underlying enum type definition. For example, this cast will sign extend because
the source type for the enum is signed. (See
[numerical conversions](#numerical-conversions) for the full description of
extension/truncation behavior.)

### Tuple Type

A tuple is a fixed-size ordered set, containing elements of heterogeneous types.
Tuple elements can be any type, e.g. bits, arrays, structs, tuples. Tuples may
be empty (an empty tuple is also known as the unit type), or contain one or more
types.

### Struct Types

Structures are similar to tuples, but provide two additional capabilities: we
name the slots (i.e. struct fields have names while tuple elements only have
positions), and we introduce a new type.

### Static Type Checking

All expressions in the language's expression grammar have a deductive type
inference rule. The types must be known for inputs to an operator/function and every
expression has a way to determine its type from its operand expressions.

### Operator Precedence

DSLX's operator precedence matches Rust's.

### Testing and Debugging

Unit tests are specified by the `test` directive, as seen below:

```dslx
#[test]
fn test_reverse() {
 assert_eq(u1:1, rev(u1:1));
 assert_eq(u2:0b10, rev(u2:0b01));
 assert_eq(u2:0b00, rev(u2:0b00));
}
```

