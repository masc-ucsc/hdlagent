**User:** DSLX Reference
Overview
DSLX is a domain specific, dataflow-oriented functional language used to build hardware that can also run effectively as host software. Within the XLS project, DSLX is also referred to as "the DSL". The DSL targets the XLS compiler (via conversion to XLS IR) to enable flows for FPGAs and ASICs.

DSLX mimics Rust, while being an immutable expression-based dataflow DSL with hardware-oriented features; e.g. arbitrary bitwidths, entirely fixed size objects, fully analyzeable call graph, etc. To avoid arbitrary new syntax/semantics choices, the DSL mimics Rust where it is reasonably possible; for example, integer conversions all follow the same semantics as Rust.

Note: There are some unnecessary differences today from Rust syntax due to early experimentation, but they are quickly being removed to converge on Rust syntax.

Note that other frontends to XLS core functionality will become available in the future; e.g. xlscc, for users familiar with the C++-and-pragma style of HLS computation. XLS team develops the DSL as part of the XLS project because we believe it can offer significant advantages over the C++-with-pragmas approach.

Dataflow DSLs are a good fit for describing hardware, compared to languages whose design assumes von Neumann style computation (global mutable state, sequential mutation by a sequential thread of control). Using a Domain Specific Language (DSL) provides a more hardware-oriented representation of a given computation that matches XLS compiler (IR) constructs closely. The DSL also allows an exploration of HLS without being encumbered by C++ language or compiler limitations such as non-portable pragmas, magic macros, or semantically important syntactic conventions. The language is still experimental and likely to change, but it is already useful for experimentation and exploration.

This document provides a reference for DSLX, mostly by example. Before perusing it in detail, we recommend you first read the DSLX tutorials to understand the broad strokes of the language.

In this document we use the function to compute a CRC32 checksum to describe language features.

Comments:
Just as in languages like Rust/C++, comments start with `//` and last through the end of the line.

Identifiers:
All identifiers, eg., for function names, parameters, and values, follow the typical naming rules of other languages. The identifiers can start with a character or an underscore, and can then contain more characters, underscores, or numbers. Valid examples are:
```
a                 // valid
CamelCase         // valid
like_under_scores // valid
__also_ok         // valid
_Ok123_321        // valid
_                 // valid

2ab               // not valid
&ade              // not valid
```
However, we suggest the following DSLX style rules, which mirror the Rust naming conventions.

Functions are `written_like_this`
User-defined data types are `NamesLikeThis`
Constant bindings are `NAMES_LIKE_THIS`
`_` is the "black hole" identifier -- a name that you can bind to but should never read from, akin to Rust's wildcard pattern match or Python's "unused identifier" convention. It should never be referred to in an expression except as a "sink".
NOTE Since mutable locals are not supported, there is also support for "tick identifiers", where a ' character may appear anywhere after the first character of an identifier to indicate "prime"; e.g. `let state' = update(state);`. By convention ticks usually come at the end of an identifier. Since this is not part of Rust's syntax, it is considered experimental at this time.

Functions
Function definitions begin with the keyword `fn`, followed by the function name, a parameter list to the function in parenthesis, followed by an `->` and the return type of the function. After this, curly braces denote the begin and end of the function body.
The list of parameters can be empty.

A single input file can contain many functions.

Simple examples:
```
fn ret3() -> u32 {
   u32:3   // This function always returns 3.
}

fn add1(x: u32) -> u32 {
   x + u32:1  // Returns x + 1, but you knew that!
}
```
Functions return the result of their last computed expression as their return value. There are no explicit return statements. By implication, functions return exactly one expression; they can't return multiple expressions (but this may change in the future as we migrate towards some Rust semantics).

Tuples should be returned if a function needs to return multiple values.

Parameters:
Parameters are written as pairs `name` followed by a colon `:` followed by the `type` of that parameter. Each parameter needs to declare its own type.

Examples:
```
// a simple parameter x of type u32
   x: u32

// t is a tuple with 2 elements.
//   the 1st element is of type u32
//   the 2nd element is a tuple with 3 elements
//       the 1st element is of type u8
//       the 2nd element is another tuple with 1 element of type u16
//       the 3rd element is of type u8
   t: (u32, (u8, (u16,), u8))
```
Parametric Functions:
DSLX functions can be parameterized in terms of the types of its arguments and in terms of types derived from other parametric values. For instance:
```
fn double(n: u32) -> u32 {
  n * u32:2
}

fn self_append<A: u32, B: u32 = {double(A)}>(x: bits[A]) -> bits[B] {
  x++x
}

fn main() -> bits[10] {
  self_append(u5:1)
}
```
In `self_append(bits[5]:1)`, we see that `A = 5` based off of formal argument instantiation. Using that value, we can evaluate `B = double(A=5)`. This derived expression is analogous to C++'s constexpr – a simple expression that can be evaluated at that point in compilation. Note that the expression must be wrapped in `{}` curly braces.
Explicit parametric instantiation:
In some cases, parametric values cannot be inferred from function arguments, such as in the `explicit_parametric_simple.x` test:
```
fn add_one<E:u32, F:u32, G:u32 = E+F>(lhs: bits[E]) -> bits[G] { ... }
```
For this call to instantiable, both `E` and `F` must be specified. Since `F` can't be inferred from an argument, we must rely on explicit parametrics:
```
  add_one<u32:1, {u32:2 + u32:3}>(u1:1);
```
This invocation will bind `1` to `E`, `5` to `F`, and `6` to `G`. Note the curly braces around the expression-defined parametric: simple literals and constant references do not need braces (but they can have them), but any other expression requires them.

EXPRESSION AMBIGUITY
Without curly braces, explicit parametric expressions could be ambiguous; consider the following, slightly changed from the previous example:
```
  add_one<u32:1, u32:2>(u32:3)>(u1:1);
```
Is the statement above computing `add_one<1, (2 > 3)>(1)`, or is it computing `(add_one<1, 2>(3)) > 1)`? Without additional (and subtle and perhaps surprising) contextual precedence rules, this would be ambiguous and could lead to a parse error or, even worse, unexpected behavior.
Fortunately, we can look to Rust for inspiration. Rust's const generics RPF introduced the `{ }` syntax for disambiguating just this case in generic specifications. With this, any expressions present in a parametric specification must be contained within curly braces, as in the original example.

At present, if the braces are omitted, some unpredictable error will occur.

Function Calls:
Function calls are expressions and look and feel just like one would expect from other languages. For example:
```
fn callee(x: bits[32], y: bits[32]) -> bits[32] {
  x + y
}
fn caller() -> u32 {
  callee(u32:2, u32:3)
}
```
If more than one value should be returned by a function, a tuple type should be returned.

