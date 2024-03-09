```
# DSLX Reference

### Overview

DSLX is a domain specific, dataflow-oriented functional language used to build
hardware that can also run effectively as host software. Within the XLS project,
DSLX is also referred to as "the DSL". The DSL targets the XLS compiler (via
conversion to XLS IR) to enable flows for FPGAs and ASICs.

DSLX mimics Rust, while being an immutable expression-based dataflow DSL with
hardware-oriented features; e.g. arbitrary bitwidths, entirely fixed size
objects, fully analyzeable call graph, etc. To avoid arbitrary new
syntax/semantics choices, the DSL mimics Rust where it is reasonably possible;
for example, integer conversions all follow the same semantics as Rust.

Note: There are *some* unnecessary differences today from Rust syntax due to
early experimentation, but they are quickly being removed to converge on Rust
syntax.

Note that other frontends to XLS core functionality will become available in the
future; e.g. [xlscc](https://github.com/google/xls/tree/main/xls/contrib/xlscc), for users
familiar with the C++-and-pragma style of HLS computation. XLS team develops the
DSL as part of the XLS project because we believe it can offer significant
advantages over the C++-with-pragmas approach.

Dataflow DSLs are a good fit for describing hardware, compared to languages
whose design assumes
[von Neumann style computation](https://en.wikipedia.org/wiki/Von_Neumann_architecture)
(global mutable state, sequential mutation by a sequential thread of control).
Using a Domain Specific Language (DSL) provides a more hardware-oriented
representation of a given computation that matches XLS compiler (IR) constructs
closely. The DSL also allows an exploration of HLS without being encumbered by
C++ language or compiler limitations such as non-portable pragmas, magic macros,
or semantically important syntactic conventions. The language is still
experimental and likely to change, but it is already useful for experimentation
and exploration.

This document provides a reference for DSLX, mostly by example. Before perusing
it in detail, we recommend you first read the
[DSLX tutorials](./tutorials/index.md)
to understand the broad strokes of the language.

In this document we use the function to compute a CRC32 checksum to describe
language features. The full code is in
[`examples/dslx_intro/crc32_one_byte.x`](https://github.com/google/xls/tree/main/xls/examples/dslx_intro/crc32_one_byte.x).

### Comments

Just as in languages like Rust/C++, comments start with `//` and last through
the end of the line.

### Identifiers

All identifiers, eg., for function names, parameters, and values, follow the
typical naming rules of other languages. The identifiers can start with a
character or an underscore, and can then contain more characters, underscores,
or numbers. Valid examples are:

```
a                // valid
CamelCase        // valid
like_under_scores // valid
__also_ok        // valid
_Ok123_321       // valid
_                // valid

2ab              // not valid
&ade             // not valid
```

However, we suggest the following **DSLX style rules**, which mirror the
[Rust naming conventions](https://doc.rust-lang.org/1.0.0/style/style/naming/README.html).

*  Functions are `written_like_this`

*  User-defined data types are `NamesLikeThis`

*  Constant bindings are `NAMES_LIKE_THIS`

*  `_` is the "black hole" identifier -- a name that you can bind to but should
   never read from, akin to Rust's wildcard pattern match or Python's "unused
   identifier" convention. It should never be referred to in an expression
   except as a "sink".

NOTE Since mutable locals are not supported, there is also
[support for "tick identifiers"](https://github.com/google/xls/issues/212),
where a ' character may appear anywhere after the first character of an
identifier to indicate "prime"; e.g. `let state' = update(state);`. By
convention ticks usually come at the end of an identifier. Since this is not
part of Rust's syntax, it is considered experimental at this time.

#### Unused Bindings

If you bind a name and do not use it, a warning will be flagged, and warnings
are errors by default; e.g. this will flag an unused warning:

```dslx
fn my_test() {
   let x = u32:42; // Not used!
}
```

For cases where it's more readable to *keep* a name, even though it's unused,
you can prefix the name with a leading underscore, like so:

```dslx
fn my_test() {
   let (thing_one, _thing_two) = open_crate();
   assert_eq(thing_one, u32:1);
}
```

Note that `_thing_two` is unused, but a warning is not flagged because we
indicated via a leading underscore that it was ok for the variable to go unused,
because we felt it enhanced readability.

### Functions

Function definitions begin with the keyword `fn`, followed by the function name,
a parameter list to the function in parenthesis, followed by an `->` and the
return type of the function. After this, curly braces denote the begin and end
of the function body.

The list of parameters can be empty.

Simple examples:

```dslx
fn ret3() -> u32 {
  u32:3  // This function always returns 3.
}

fn add1(x: u32) -> u32 {
  x + u32:1 // Returns x + 1, but you knew that!
}
```

Functions return the result of their last computed expression as their return
value. There are no explicit return statements. By implication, functions return
exactly one expression; they can't return multiple expressions (but this may
change in the future as we migrate towards some Rust semantics).

Tuples should be returned if a function needs to return multiple values.

### Parameters

Parameters are written as pairs `name` followed by a colon `:` followed by the
`type` of that parameter. Each parameter needs to declare its own type.

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

DSLX functions can be parameterized in terms of the types of its arguments and
in terms of types derived from other parametric values. For instance:

```dslx
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

In `self_append(bits[5]:1)`, we see that `A = 5` based off of formal argument
instantiation. Using that value, we can evaluate `B = double(A=5)`. This derived
expression is analogous to C++'s constexpr – a simple expression that can be
evaluated at that point in compilation. Note that the expression must be wrapped
in `{}` curly braces.

See
[advanced understanding](#advanced-understanding-parametricity-constraints-and-unification)
for more information on parametricity.

#### Explicit parametric instantiation

In some cases, parametric values cannot be inferred from function arguments,
such as in the
[`explicit_parametric_simple.x`](https://github.com/google/xls/tree/main/xls/dslx/tests/explicit_parametric_simple.x)
test:

```
fn add_one<E:u32, F:u32, G:u32 = E+F>(lhs: bits[E]) -> bits[G] { ... }
```

For this call to instantiable, both `E` and `F` must be specified. Since `F`
can't be inferred from an argument, we must rely on _explicit parametrics_:

```dslx
 add_one<u32:1, {u32:2 + u32:3}>(u1:1);
```

This invocation will bind `1` to `E`, `5` to `F`, and `6` to `G`. Note the curly
braces around the expression-defined parametric: simple literals and constant
references do not need braces (but they _can_ have them), but any other
expression requires them.

##### Expression ambiguity

Without curly braces, explicit parametric expressions could be ambiguous;
consider the following, slightly changed from the previous example:

```dslx
 add_one<u32:1, u32:2>(u32:3)>(u1:1);
```

Is the statement above computing `add_one<1, (2 > 3)>(1)`, or is it computing
`(add_one<1, 2>(3)) > 1)`? Without additional (and subtle and perhaps surprising)
contextual precedence rules, this would be ambiguous and could lead to a parse
error or, even worse, unexpected behavior.

Fortunately, we can look to Rust for inspiration. Rust's const generics RPF
introduced the `{ }` syntax for disambiguating just this case in generic
specifications. With this, any expressions present in a parametric specification
must be contained within curly braces, as in the original example.

At present, if the braces are omitted, some unpredictable error will occur. Work
to improve this is tracked in
[XLS GitHub issue #321](https://github.com/google/xls/issues/321).

### Function Calls

Function calls are expressions and look and feel just like one would expect from
other languages. For example:

```dslx
fn callee(x: bits[32], y: bits[32]) -> bits[32] {
 x + y
}
fn caller() -> u32 {
 callee(u32:2, u32:3)
}
```

If more than one value should be returned by a function, a tuple type should be
returned.

### Built-In Functions and Standard Library

The DSL has several built-in functions and standard library modules. For details
on the available functions to invoke, see
[DSLX Built-In Functions and Standard Library](./dslx_std.md).

## Types

### Bit Type

The most fundamental type in DSLX is a variable length bit type denoted as
`bits[n]`, where `n` is a constant. For example:

```
bits[1]  // a single bit
uN[1]    // explicitly noting single bit is unsigned
u1       // convenient shorthand for bits[1]

bits[8]  // an 8-bit datatype, yes, a byte
u8       // convenient shorthand for bits[8]
bits[32] // a 32-bit datatype
u32      // convenient shorthand for bits[32]
bits[256] // a 256-bit datatype

bits[0]  // possible, but, don't do that
```

DSLX introduces aliases for commonly used types, such as `u8` for an 8-wide bit
type, or `u32` for a 32-bit wide bit type. These are defined up to `u64`.

All `u*`, `uN[*]`, and `bits[*]` types are interpreted as unsigned integers.
Signed integers are specified via `s*` and `sN[*]`. Similarly to unsigned
numbers, the `s*` shorthands are defined up to `s64`. For example:

```
sN[1]
s1

sN[64]
s64

sN[256]

sN[0]
s0
```

Signed numbers differ in their behavior from unsigned numbers primarily via
operations like comparisons, (variable width) multiplications, and divisions.

#### Bit Type Attributes

Bit types have helpful type-level attributes that provide limit values, similar
to `std::numeric_limits` in C++. For example:

```dslx
u3::MAX  // u3:0b111 the "fill with ones" value
s3::MAX  // s3:0b011 the "maximum signed" value

u3::ZERO // u3:0b000 the "fill with zeros" value
s3::ZERO // s3:0b000 the "fill with zeros" value
```

#### Character Constants

Characters are a special case of bits types: they are implicitly-type as u8.
Characters can be used just as traditional bits:

```dslx
fn add_to_null(input: u8) -> u8 {
 let null:u8 = '\0';
 input + null
}

#[test]
fn test_main() {
 assert_eq('a', add_to_null('a'))
}
```

DSLX character constants support the
[full Rust set of escape sequences](https://doc.rust-lang.org/reference/tokens.html) with the exception of unicode.

### Enum Types

DSLX supports enumerations as a way of defining a group of related, scoped,
named constants that do not pollute the module namespace. For example:

```dslx
enum Opcode : u3 {
 FIRE_THE_MISSILES = 0,
 BE_TIRED = 1,
 TAKE_A_NAP = 2,
}

fn get_my_favorite_opcode() -> Opcode {
 Opcode::FIRE_THE_MISSILES
}
```

Note the use of the double-colon to reference the enum value. This code
specifies that the enum behaves like a `u3`: its storage and extension (via
casting) behavior are defined to be those of a `u3`. Attempts to define an enum
value outside of the representable `u3` range will produce a compile time error.

```dslx-bad
enum Opcode : u3 {
 FOO = 8 // Causes compile time error!
}
```

Enums can be compared for equality/inequality, but they do not permit arithmetic
operations, they must be cast to numerical types in order to perform arithmetic:

```dslx
enum Opcode: u3 {
 NOP = 0,
 ADD = 1,
 SUB = 2,
 MUL = 3,
}

fn same_opcode(x: Opcode, y: Opcode) -> bool {
 x == y // ok
}

fn next_in_sequence(x: Opcode, y: Opcode) -> bool {
 x+1 == (y as u3) // ok, casted first
}
```

As mentioned above, casting of enum-values works with the same casting/extension
rules that apply to the underlying enum type definition. For example, this cast
will sign extend because the source type is signed. (See
[numerical conversions](#numerical-conversions) for the full description of
extension/truncation behavior.)

```dslx
enum MySignedEnum : s3 {
 LOW = -1,
 ZERO = 0,
 HIGH = 1,
}

fn extend_to_32b(x: MySignedEnum) -> u32 {
 x as u32 // Sign-extends because the source type is signed.
}

#[test]
fn test_extend_to_32b() {
 assert_eq(extend_to_32b(MySignedEnum::LOW), u32:0xffffffff)
}
```

Casting *to* an enum is also permitted. However, in most cases errors from
invalid casting can only be found at runtime, e.g., in the DSL interpreter or
flagging a fatal error from hardware. Because of that, it is recommended to
avoid such casts as much as possible.

### Tuple Type

A tuple is a fixed-size ordered set, containing elements of heterogeneous types.
Tuples elements can be any type, e.g. bits, arrays, structs, tuples. Tuples may
be empty (an empty tuple is also known as the unit type), or contain one or more
types.

Examples of tuple values:

```dslx
// The unit type, carries no information.
let unit = ();

// A tuple containing two bits-typed elements.
let pair = (u3:0b100, u4:0b1101);
```

Example of a tuple type:

```dslx
// The type of a tuple with 2 elements.
//  the 1st element is of type u32
//  the 2nd element is a tuple with 3 elements
//      the 1st element is of type u8
//      the 2nd element is another tuple with 1 element of type u16
//      the 3rd element is of type u8
type MyTuple = (u32, (u8, (u16,), u8));
```

To access individual tuple elements use simple indices, starting at 0. For
example, to access the second element of a tuple (index 1):

```dslx
#[test]
fn test_tuple_access() {
 let t = (u32:2, u8:3);
 assert_eq(u8:3, t.1)
}
```

Such indices can only be numeric literals; parametric symbols are not allowed.

Tuples can be "destructured", similarly to how pattern matching works in `match`
expressions, which provides a convenient syntax to name elements of a tuple for
subsequent use. See `a` and `b` in the following:

```dslx
#[test]
fn test_tuple_destructure() {
 let t = (u32:2, u8:3);
 let (a, b) = t;
 assert_eq(u32:2, a);
 assert_eq(u8:3, b)
}
```

Just as values can be discarded in a `let` by using the "black hole identifier"
`_`, don't-care values can also be discarded when destructuring a tuple:

```dslx
#[test]
fn test_black_hole() {
 let t = (u32:2, u8:3, true);
 let (_, _, v) = t;
 assert_eq(v, true)
}
```

### Struct Types

Structures are similar to tuples, but provide two additional capabilities: we
name the slots (i.e. struct fields have names while tuple elements only have
positions), and we introduce a new type.

The following syntax is used to define a struct:

```dslx
struct Point {
 x: u32,
 y: u32,
}
```

Once a struct is defined it can be constructed by naming the fields in any
order:

```dslx
struct Point {
 x: u32,
 y: u32,
}

#[test]
fn test_struct_equality() {
 let p0 = Point { x: u32:42, y: u32:64 };
 let p1 = Point { y: u32:64, x: u32:42 };
 assert_eq(p0, p1)
}
```

There is a simple syntax when creating a struct whose field names match the
names of in-scope values:

```dslx
struct Point { x: u32, y: u32, }

#[test]
fn test_struct_equality() {
 let x = u32:42;
 let y = u32:64;
 let p0 = Point { x, y };
 let p1 = Point { y, x };
 assert_eq(p0, p1)
}
```

Struct fields can also be accessed with "dot" syntax:

```dslx
struct Point {
 x: u32,
 y: u32,
}

fn f(p: Point) -> u32 {
 p.x + p.y
}

fn main() -> u32 {
 f(Point { x: u32:42, y: u32:64 })
}

#[test]
fn test_main() {
 assert_eq(u32:106, main())
}
```

Note that structs cannot be mutated "in place", the user must construct new
values by extracting the fields of the original struct mixed together with new
field values, as in the following:

```dslx
struct Point3 {
 x: u32,
 y: u32,
 z: u32,
}

fn update_y(p: Point3, new_y: u32) -> Point3 {
 Point3 { x: p.x, y: new_y, z: p.z }
}

fn main() -> Point3 {
 let p = Point3 { x: u32:42, y: u32:64, z: u32:256 };
 update_y(p, u32:128)
}

#[test]
fn test_main() {
 let want = Point3 { x: u32:42, y: u32:128, z: u32:256 };
 assert_eq(want, main())
}
```

#### Struct Update Syntax

The DSL has syntax for conveniently producing a new value with a subset of
fields updated to reduce verbosity. The "struct update" syntax is:

```dslx
struct Point3 {
 x: u32,
 y: u32,
 z: u32,
}

fn update_y(p: Point3) -> Point3 {
 Point3 { y: u32:42, ..p }
}

fn update_x_and_y(p: Point3) -> Point3 {
 Point3 { x: u32:42, y: u32:42, ..p }
}
```

#### Understanding Nominal Typing

As mentioned above, a struct definition introduces a new type. Structs are
nominally typed, as opposed to structurally typed (note that tuples are
structurally typed). This means that structs with different names have different
types, regardless of whether those structs have the same structure (i.e. even
when all the fields of two structures are identical, those structures are a
different type when they have a different name).

```dslx
struct Point {
 x: u32,
 y: u32,
}

struct Coordinate {
 x: u32,
 y: u32,
}

fn f(p: Point) -> u32 {
 p.x + p.y
}

#[test]
fn test_ok() {
 assert_eq(f(Point { x: u32:42, y: u32:64 }), u32:106)
}
```

```dslx-bad
#[test]
fn test_type_checker_error() {
 assert_eq(f(Coordinate { x: u32:42, y: u32:64 }), u32:106)
}
```

### Array Type

Arrays can be constructed via bracket notation. All values that make up the
array must have the same type. Arrays can be indexed with indexing notation
(`a[i]`) to retrieve a single element.

```dslx
fn main(a: u32[2], i: u1) -> u32 {
 a[i]
}

#[test]
fn test_main() {
 let x = u32:42;
 let y = u32:64;
 // Make an array with "bracket notation".
 let my_array: u32[2] = [x, y];
 assert_eq(main(my_array, u1:0), x);
 assert_eq(main(my_array, u1:1), y);
}
```

Because arrays with repeated trailing elements are common, the DSL supports
ellipsis (`...`) at the end of an array to fill the remainder of the array with
the last noted element. Because the compiler must know how many elements to
fill, in order to use the ellipsis the type must be annotated explicitly as
shown.

```dslx
fn make_array(x: u32) -> u32[3] {
 u32[3]:[u32:42, x, ...]
}

#[test]
fn test_make_array() {
 assert_eq(u32[3]:[u32:42, u32:42, u32:42], make_array(u32:42));
 assert_eq(u32[3]:[u32:42, u32:64, u32:64], make_array(u32:64));
}
```

Note [google/xls#917](https://github.com/google/xls/issues/917): arrays with
length zero will typecheck, but fail to work in most circumstances. Eventually,
XLS should support them but they can't be used currently.

TODO(meheff): Explain arrays and the intricacies of our bits type interpretation
and how it affects arrays of bits etc.

#### Character String Constants

Character strings are a special case of array types, being implicitly-sized
arrays of u8 elements. String constants can be used just as traditional arrays:

```dslx
fn add_one<N: u32>(input: u8[N]) -> u8[N] {
 for (i, result) : (u32, u8[N]) in u32:0..N {
   update(result, i, result[i] + u8:1)
 }(input)
}

#[test]
fn test_main() {
 assert_eq("bcdef", add_one("abcde"))
}
```

DSLX string constants support the
[full Rust set of escape sequences](https://doc.rust-lang.org/reference/tokens.html) -
note that unicode escapes get encoded to their UTF-8 byte sequence. In other
words, the sequence `\u{10CB2F}` will result in an array with hexadecimal values
`F4 8C AC AF`.

Moreover, string can be composed of [characters](#character-constants).

```dslx
fn string_composed_characters() -> u8[10] {
 ['X', 'L', 'S', ' ', 'r', 'o', 'c', 'k', 's', '!']
}

#[test]
fn test_main() {
 assert_eq("XLS rocks!", string_composed_characters())
}
```

### Type Aliases

DLSX supports the definition of type aliases.

Type aliases can be used to provide a more human-readable name for an existing
type. The new name is on the left, the existing name on the right:

```dslx
type Weight = u6;
```

We can create an alias for an imported type:

```dslx
// Note: this imports an external file in the codebase.
import xls.dslx.tests.mod_imported;

type MyEnum = mod_imported::MyEnum;

fn main(x: u8) -> MyEnum {
 x as MyEnum
}

#[test]
fn test_main() {
 assert_eq(main(u8:42), MyEnum::FOO);
 assert_eq(main(u8:64), MyEnum::BAR);
}
```

Type aliases can also provide a descriptive name for a tuple type (which is
otherwise anonymous). For example, to define a tuple type that represents a
float number with a sign bit, an 8-bit mantissa, and a 23-bit mantissa, one
would write:

```dslx
type F32 = (u1, u8, u23);
```

After this definition, the `F32` may be used as a type annotation
interchangeably with `(u1, u8, u23)`.

Note, however, that structs are generally preferred for this purpose, as they
are more readable and users do not need to rely on tuple elements having a
stable order in the future (i.e., they are resilient to refactoring).

### Type Casting

Bit types can be cast from one bit-width to another with the `as` keyword. Types
can be widened (increasing bit-width), narrowed (decreasing bit-width) and/or
changed between signed and unsigned. Some examples are found below. See
[Numerical Conversions](#numerical-conversions) for a description of the
semantics.

```dslx
#[test]
fn test_narrow_cast() {
 let twelve = u4:0b1100;
 assert_eq(twelve as u2, u2:0)
}

#[test]
fn test_widen_cast() {
 let three = u2:0b11;
 assert_eq(three as u4, u4:3)
}

#[test]
fn test_narrow_signed_cast() {
 let negative_seven = s4:0b1001;
 assert_eq(negative_seven as u2, u2:1)
}

#[test]
fn test_widen_to_unsigned() {
 let negative_one = s2:0b11;
 assert_eq(negative_one as u3, u3:0b111)
}

#[test]
fn test_widen_to_signed() {
 let three = u2:0b11;
 assert_eq(three as u3, u3:0b011)
}
```

### Type Checking and Inference

DSLX performs type checking and produces an error if types in an expression
don't match up.

`let` expressions also perform type inference, which is quite convenient. For
example, instead of writing:

```dslx-snippet
let ch: u32 = (e & f) ^ ((!e) & g);
let (h, g, f): (u32, u32, u32) = (g, f, e);
```

one can write the following, as long as the types can be properly inferred:

```dslx-snippet
let ch = (e & f) ^ ((!e) & g);
let (h, g, f) = (g, f, e);
```

Note that type annotations can still be added and be used for program
understanding, as they they will be checked by DSLX.

### Type Inference Details

#### Type Inference Background

All expressions in the language's expression grammar have a deductive type
inference rule. The types must be known for inputs to an
operator/function[^usebeforedef] and every expression has a way to determine its
type from its operand expressions.

[^usebeforedef]: Otherwise there'd be a use-before-definition error.

DSLX uses deductive type inference to check the types present in the program.
Deductive type inference is a set of (typically straight-forward) deduction
rules: Hindley-Milner style deductive type inference determines the result type
of a function with a rule that only observes the input types to that function.
(Note that operators like '+' are just slightly special functions in that they
have pre-defined special-syntax-rule names.)

#### Bindings and Environment

In DSLX code, the "environment" where names are bound (sometimes also referred
to as a symbol table) is called the
[`Bindings`](https://github.com/google/xls/tree/main/xls/dslx/frontend/bindings.h) -- it
maps identifiers to the AST node that defines the name (`{string: AstNode}`),
which can be combined with a mapping from AST node to its deduced type
(`{AstNode: ConcreteType}`) to resolve the type of an identifier in the program.
`Let` is one of the key nodes that populates these `Bindings`, but anything that
creates a bound name does as well (e.g. parameters, for loop induction
variables, etc.).

#### Operator Example

For example, consider the binary (meaning takes two operands) '/' operator. The
simple deductive type inference rule for '/' is:

`(T, T) -> T`

Meaning that the left hand side operand to the '/' operator is of some type
(call it T), the right hand side operand to the '/' operator must be of that
same type, T, and the result of that operator is then (deduced) to be of the
same type as its operands, T.

Let's instantiate this rule in a function:

```dslx
fn add_wrapper(x: bits[2], y: bits[2]) -> bits[2] {
 x + y
}
```

This function wraps the '+' operator. It presents two arguments to the '+'
operator and then checks that the annotated return type on `add_wrapper` matches
the deduced type for the body of that function; that is, we ask the following
question of the '+' operator (since the type of the operands must be known at
the point the add is performed):

`(bits[2], bits[2]) -> ?`

To resolve the '?' the following procedure is being used:

*  Pattern match the rule given above `(T, T) -> T` to determine the type T:
   the left hand side operand is `bits[2]`, called T.
*  Check that the right hand side is also that same T, which it is: another
   `bits[2]`.
*  Deduce that the result type is that same type T: `bits[2]`.
*  That becomes the return type of the body of the function. Check that it is
   the same type as the annotated return type for the function, and it is!

The function is annotated to return `bits[2]`, and the deduced type of the body
is also `bits[2]`. Qed.

#### Let Bindings, Names, and the Environment

In the DSL, `let` is an expression. It may not seem obvious at a glance, but it
is! As a primer see the [type inference background](#type-inference-background)
and how [names are resolved in an environment](#bindings-and-environment).

"let" expressions are of the (Rust-inspired) form:

`let $name: $annotated_type = $expr; $subexpr`

`$name` gets "bound" to a value of type `$annotated_type`. The `let` typecheck
rule must **both** check that `$expr` is of type `$annotated_type`, as well as
determine the type of `$subexpr`, which is the type of the overall "let
expression".

In this example, the result of the `let` expression is the return value --
`$subexpr` (`x+x... (The response was truncated because it has reached the token limit. Try to increase the token limit if you need a longer response.)

