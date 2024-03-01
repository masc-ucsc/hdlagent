**User:** Statements:

Imports:
DSLX modules can import other modules via the `import` keyword. Circular imports are not permitted (the dependencies among DSLX modules must form a DAG, as in languages like Go).

The import statement takes the following form (note the lack of semicolon):
```
import path.to.my.imported_module
```
With that statement, the module will be accessible as (the trailing identifier after the last dot) `imported_module`; e.g. the program can refer to `imported_module::IMPORTED_MODULE_PUBLIC_CONSTANT`.

NOTE Imports are relative to the Bazel "depot root" -- for external use of the tools a `DSLX_PATH` will be exposed, akin to a `PYTHONPATH`, for users to indicate paths where were should attempt module discovery.

NOTE Importing does not introduce any names into the current file other than the one referred to by the import statement. That is, if `imported_module` had a constant defined in it `FOO`, this is referred to via `imported_module::FOO`, `FOO` does not "magically" get put in the current scope. This is analogous to how wildcard imports are discouraged in other languages (e.g. `from import *` in Python) on account of leading to "namespace pollution" and needing to specify what happens when names conflict.

If you want to change the name of the imported module (for reference inside of the importing file) you can use the `as` keyword:
```
import path.to.my.imported_module as im
```
Just using the above construct, `imported_module::IMPORTED_MODULE_PUBLIC_CONSTANT` is not valid, only `im::IMPORTED_MODULE_PUBLIC_CONSTANT`. However, both statements can be used on different lines:
```
import path.to.my.imported_module
import path.to.my.imported_module as im
```
In this case, either `im::IMPORTED_MODULE_PUBLIC_CONSTANT` or `imported_module::IMPORTED_MODULE_PUBLIC_CONSTANT` can be used to refer to the same thing.

Here is an example using the same function via two different aliases for the same module:
```
// Note: this imports an external file in the codebase under two different
// names.
import xls.dslx.tests.mod_imported
import xls.dslx.tests.mod_imported as mi

fn main(x: u3) -> u1 {
  mod_imported::my_lsb(x) || mi::my_lsb(x)
}

#[test]
fn test_main() {
  assert_eq(u1:0b1, main(u3:0b001))
}
```
Public module members:
Module members are private by default and not accessible from any importing module. To make a member public/visible to importing modules, the `pub` keyword must be added as a prefix; e.g.
```
const FOO = u32:42;      // Not accessible to importing modules.
pub const BAR = u32:64;  // Accessible to importing modules.
```
This applies to other things defined at module scope as well: functions, enums, type aliases, etc.
```
import xls.dslx.tests.mod_imported
import xls.dslx.tests.mod_imported as mi

fn main(x: u3) -> u1 {
  mod_imported::my_lsb(x) || mi::my_lsb(x)
}

#[test]
fn test_main() {
  assert_eq(u1:0b1, main(u3:0b001))
}
```

Const:
The `const` keyword is used to define module-level constant values. Named constants should be usable anywhere a literal value can be used:
```
const FOO = u8:42;

fn match_const(x: u8) -> u8 {
  match x {
    FOO => u8:0,
    _ => u8:42,
  }
}

#[test]
fn test_match_const_not_binding() {
  assert_eq(u8:42, match_const(u8:0));
  assert_eq(u8:42, match_const(u8:1));
  assert_eq(u8:0, match_const(u8:42));
}

fn h(t: (u8, (u16, u32))) -> u32 {
  match t {
    (FOO, (x, y)) => (x as u32) + y,
    (_, (y, u32:42)) => y as u32,
    _ => u32:7,
  }
}

#[test]
fn test_match_nested() {
  assert_eq(u32:3, h((u8:42, (u16:1, u32:2))));
  assert_eq(u32:1, h((u8:0, (u16:1, u32:42))));
  assert_eq(u32:7, h((u8:0, (u16:1, u32:0))));
}
```
Expressions:

Literals:
DSLX supports construction of literals using the syntax `Type:Value`. For example `u16:1` is a 16-wide bit array with its least significant bit set to one. Similarly `s8:12` is an 8-wide bit array with its least significant four bits set to `1100`.

DSLX supports initializing using binary, hex or decimal syntax. So
```
#[test]
fn test_literal_initialization() {
  assert_eq(u8:12, u8:0b00001100);
  assert_eq(u8:12, u8:0x0c);
}
```
When constructing literals DSLX will trigger an error if the constant will not fit in a bit array of the annotated sized, so for example trying to construct the literal `u8:256` will trigger an error of the form:
```
TypeInferenceError: uN[8] Value '256' does not fit in the bitwidth of a uN[8] (8)
```
But what about `s8:128` ? This is a valid literal, even though a signed 8-bit integer cannot represent it. The following code offers a clue.
```
#[test]
fn test_signed_literal_initialization() {
  assert_eq(s8:128, s8:-128);
  assert_eq(s8:128, s8:0b10000000);
}
```
What is happening here is that, 128 is being used as a bit pattern rather than as the number 128 to initialize the literal. It is only when the bit pattern cannot fit in the width of the literal that an error is triggered.

Note that behaviour is different from Rust, where it will trigger an error, and the fact that DSLX considers this valid may change in the future.

Unary Expressions:
DSLX supports three types of unary expressions:

	bit-wise not (the `!` operator)
	negate (the `-` operator, computes the two's complement negation)

Binary Expressions:
DSLX supports a familiar set of binary expressions. There are two categories of binary expressions. A category where both operands to the expression must be of the same bit type (i.e., not arrays or tuples), and a category where the operands can be of arbitrary bit types (i.e. shift expressions).

shift-right (`>>`)
shift-left (`<<`)
bit-wise or (`|`)
bit-wise and (`&`)
add (`+`)
subtract (`-`)
xor (`^`)
multiply (`*`)
logical or (`||`)
logical and (`&&`)

Shift Expressions:
Shift expressions include: shift-right (logical) and shift-left. These are binary operations that don't require the same type on the left and right hand side. The right hand side must be unsigned, but it does not need to be the same type or width as the left hand side, i.e. the type signature for these operations is: `(xN[M], uN[N]) -> xN[M]`. If the right hand side is a literal value it does not need to be type annotated. For example:
```
fn shr_two(x: s32) -> s32 {
  x >> 2
}
```
Note that, as in Rust, the semantics of the shift-right (`>>`) operation depends on the signedness of the left hand side. For a signed-type left hand side, the shift-right (`>>`) operation performs a shift-right arithmetic and, for a unsigned-type left hand side, the shift-right (`>>`) operation performs a shift-right (logical).

Comparison Expressions:
For comparison expressions the types of both operands must match. However these operations return a result of type `bits[1]`, aka `bool`.

equal (`==`)
not-equal (`!=`)
greater-equal (`>=`)
greater (`>`)
less-equal (`<=`)
less (`<`)

Concat Expression:
Bitwise concatenation is performed with the `++` operator. The value on the left hand side becomes the most significant bits, the value on the right hand side becomes the least significant bits. These may be chained together as shown below:
```
#[test]
fn test_bits_concat() {
  assert_eq(u8:0b11000000, u2:0b11 ++ u6:0b000000);
  assert_eq(u8:0b00000111, u2:0b00 ++ u6:0b000111);
  assert_eq(u6:0b100111, u1:1 ++ u2:0b00 ++ u3:0b111);
  assert_eq(u6:0b001000, u1:0 ++ u2:0b01 ++ u3:0b000);
  assert_eq(u32:0xdeadbeef, u16:0xdead ++ u16:0xbeef);
}
```

Block Expressions:
Block expressions enable subordinate scopes to be defined, e.g.:
```
let a = {
  let b = u32:1;
  b + u32:3
};
```
The value of a block expression is that of its last contained expression, or (), if a final expression is omitted:
```
let a = { let b = u32:1; };
```
In the above case, `a` is equal to `()`.

Since DSLX does not currently have the concept of lifetimes, and since names can be rebound (i.e., there's no concept of mutability, allowing `let a = u32:0; let a = u32:1;`), blocks are primarily for readability at this time, (side from their use as the "body" of functions and loops).

Match Expression:
Match expressions permit "pattern matching" on data, like a souped-up switch statement. It can both test for values (like a conditional guard) and bind values to identifiers for subsequent use. For example:
```
fn f(t: (u8, u32)) -> u32 {
  match t {
    (u8:42, y) => y,
    (_, y) => y+u32:77
  }
}
```
If the first member of the tuple is the value is `42`, we pass the second tuple member back as-is from the function. Otherwise, we add `77` to the value and return that. The `_` symbolizes "I don't care about this value".

Just like literal constants, pattern matching can also match via named constants; For example, consider this variation on the above:
```
const MY_FAVORITE_NUMBER = u8:42;
fn f(t: (u8, u32)) -> u32 {
  match t {
    (MY_FAVORITE_NUMBER, y) => y,
    (_, y) => y+u32:77
  }
}
```
This also works with nested tuples; for example:
```
const MY_FAVORITE_NUMBER = u8:42;
fn f(t: (u8, (u16, u32))) -> u32 {
  match t {
    (MY_FAVORITE_NUMBER, (y, z)) => y as u32 + z,
    (_, (y, u32:42)) => y as u32,
    _ => u32:7
  }
}
```
Here we use a "catch all" wildcard pattern in the last match arm to ensure the match expression always matches the input somehow.

Redundant Patterns:
`match` will flag an error if a syntactically identical pattern is typed twice; e.g.
```
const FOO = u32:42;
fn f(x: u32) -> u2 {
  match x {
    FOO => u2:0,
    FOO => u2:1,  // Identical pattern!
    _ => u2:2,
  }
}
```
Only the first pattern will ever match, so it is fully redundant (and therefore likely a user error they'd like to be informed of). Note that equivalent but not syntactically identical patterns will not be flagged in this way.
```
const FOO = u32:42;
const BAR = u32:42;  // Compares `==` to `FOO`.
fn f(x: u32) -> u2 {
  match x {
    FOO => u2:0,
    BAR => u2:1,  // _Equivalent_ pattern, but not syntactically identical.
    _ => u2:2,
  }
}
```

`let` Expression:
let expressions work the same way as let expressions in other functional languages (such as the ML family languages). let expressions provide a nested, lexically-scoped, list of binding definitions. The scope of the binding is the expression on the right hand side of the declaration. For example:
```
let a: u32 = u32:1 + u32:2;
let b: u32 = a + u32:3;
b
```
would bind (and return as a value) the value `6` which corresponds to `b` when evaluated. In effect there is little difference to other languages like C/C++ or Python, where the same result would be achieved with code similar to this:
```
a = 1 + 2
b = a + 3
return b
```
However, `let` expressions are lexically scoped. In above example, the value `3` is bound to `a` only during the combined let expression sequence. There is no other type of scoping in DSLX.

If Expression:
DSLX offers an `if` expression, which is very similar to the Rust `if` expression. Blueprint:
```
if condition { consequent } else { alternate }
```
This corresponds to the C/C++ ternary `?:` operator:
```
condition ? consequent : alternate
```
Note: both the `if` and `else` are required to be present, as with the `?:` operator, unlike a C++ `if` statement. This is because it is an expression that produces a result value, not a statement that causes a mutating effect.

Furthermore, you can have multiple branches via `else if`:
```
if condition0 { consequent0 } else if condition1 { consequent1 } else { alternate }
```
which corresponds to the C/C++:
```
condition0 ? consequent0 : (contition1 ? consequent1 : alternate)
```
Note: a `match` expression can often be a better choice than having a long `if/else if/.../else` chain.

For example, in the FP adder module (modules/fp32_add_2.x), there is code like the following:
```
[...]
let result_fraction = if wide_exponent < u9:255 { result_fraction } else { u23:0 };
let result_exponent = if wide_exponent < u9:255 { wide_exponent as u8 } else { u8:255 };
```

Iterable Expression:
Iterable expressions are used in counted for loops. DSLX currently supports two types of iterable expressions, `range` and `enumerate`.

The range expression `m..n` represents a range of values from m to n-1. This example will run from 0 to 4 (exclusive):
```
for (i, accum): (u32, u32) in u32:0..u32:4 {
```
There also exists a `range()` builtin function that performs the same operation.

`enumerate` iterates over the elements of an array type and produces pairs of `(index, value)`, similar to enumeration constructs in languages like Python or Go.

In the example below, the loop will iterate 8 times, following the array dimension of `x`. Each iteration produces a tuple with the current index (`i` ranging from 0 to 7) and the value at the index (`e = x[i]`).
```
fn prefix_scan_eq(x: u32[8]) -> bits[8,3] {
  let (_, _, result) =
    for ((i, e), (prior, count, result)): ((u32, u32), (u32, u3, bits[8,3]))
        in enumerate(x) {...
```

for Expression:
DSLX currently supports synthesis of "counted" for loops (loops that have a clear upper bound on their number of iterations). These loops are capable of being generated as unrolled pipeline stages: when generating a pipeline, the XLS compiler will unroll and specialize the iterations.

NOTE In the future support for loops with an unbounded number of iterations may be permitted, but will only be possible to synthesize as a time-multiplexed implementation, since pipelines cannot be unrolled indefinitely.
