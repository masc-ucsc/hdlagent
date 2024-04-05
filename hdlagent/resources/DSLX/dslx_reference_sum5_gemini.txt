**DSLX Reference**

**Overview**

DSLX is a dataflow-oriented functional language used to build hardware that can also run effectively as host software. Within the XLS project, DSLX is also referred to as "the DSL". The DSL targets the XLS compiler (via conversion to XLS IR) to enable flows for FPGAs and ASICs.

DSLX mimics Rust, while being an immutable expression-based dataflow DSL with hardware-oriented features; e.g. arbitrary bitwidths, entirely fixed size objects, fully analyzable call graph, etc. To avoid arbitrary new syntax/semantics choices, the DSL mimics Rust where it is reasonably possible; for example, integer conversions all follow the same semantics as Rust.

Note: There are *some* unnecessary differences today from Rust syntax due to early experimentation, but they are quickly being removed to converge on Rust syntax.

Note that other frontends to XLS core functionality will become available in the future; e.g. [xlscc](https://github.com/google/xls/tree/main/xls/contrib/xlscc), for users familiar with the C++-and-pragma style of HLS computation. XLS team develops the DSL as part of the XLS project because we believe it can offer significant advantages over the C++-with-pragmas approach.

**Comments**

Just as in languages like Rust/C++, comments start with `//` and last through the end of the line.

**Identifiers**

All identifiers, eg., for function names, parameters, and values, follow the typical naming rules of other languages. The identifiers can start with a character or an underscore, and can then contain more characters, underscores, or numbers. Valid examples are:

```
a                // valid
CamelCase        // valid
like_under_scores // valid
__also_ok        // valid
_Ok123_321       // valid

2ab              // not valid
&ade             // not valid
```

However, we suggest the following **DSLX style rules**, which mirror the [Rust naming conventions](https://doc.rust-lang.org/1.0.0/style/style/naming/README.html).

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

**Unused Bindings**

If you bind a name and do not use it, a warning will be flagged, and warnings
are errors by default; e.g. this will flag an unused warning:

```dslx-snippet
#[test]
fn my_test() {
   let x = u32:42; // Not used!
}
```

For cases where it's more readable to *keep* a name, even though it's unused,
you can prefix the name with a leading underscore, like so:

```dslx-snippet
#[test]
fn my_test() {
   let (thing_one, _thing_two) = open_crate();
   assert_eq(thing_one, u32:1);
}
```

Note that `_thing_two` is unused, but a warning is not flagged because we
indicated via a leading underscore that it was ok for the variable to go unused,
because we felt it enhanced readability.

**Functions**

Function definitions begin with the keyword `fn`, followed by the function name,
a parameter list to the function in parenthesis, followed by an `->` and the
return type of the function. After this, curly braces denote the begin and end
of the function body.

The list of parameters can be empty.

A single input file can contain many functions.

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

```dslx-snippet
 add_one<u32:1, {u32:2 + u32:3}>(u1:1);
```

This invocation will bind `1` to `E`, `5` to `F`, and `6` to `G`. Note the curly
braces around the expression-defined parametric: simple literals and constant
references do not need braces (but they _can_ have them), but any other
expression requires them.

##### Expression ambiguity

Without curly braces, explicit parametric expressions could be ambiguous;
consider the following, slightly changed from the previous example:

```dslx-snippet
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

At present, if the braces are omitted, some unpredictable error

