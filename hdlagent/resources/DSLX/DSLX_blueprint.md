**User:** Blueprint:
```
for (index, accumulator): (type-of-index, type-of-accumulator) in iterable {
   body-expression
} (initial-accumulator-value)
```
The type annotation in the above "blueprint" is optional, but often helpful to include for increased clarity.

Because DSLX is a pure dataflow description, a for loop is an expression that produces a value. As a result, you grab the output of a for loop just like any other expression:
```
let final_accum = for (i, accum) in u32:0..u32:8 {
  let new_accum = f(accum);
  new_accum
}(init_accum);
```
Conceptually the for loop "evolves" the accumulator as it iterates, and ultimately pops it out as the result of its evaluation.

Examples:
Add up all values from 0 to 4 (exclusive). Note that we pass the accumulator's initial value in as a parameter to this expression.
```
for (i, accum): (u32, u32) in u32:0..u32:4 {
  accum + i
}(u32:0)
```
To add up values from 7 to 11 (exclusive), one would write:
```
let base = u32:7;
for (i, accum): (u32, u32) in u32:0..u32:4 {
  accum + base + i
}(u32:0)
```
"Loop invariant" values (values that do not change as the loop runs) can be used in the loop body, for example, note the use of `outer_thing` below:
```
let outer_thing: u32 = u32:42;
for (i, accum): (u32, u32) in u32:0..u32:4 {
    accum + i + outer_thing
}(u32:0)
```
Both the index and accumulator can be of any valid type, in particular, the accumulator can be a tuple type, which is useful for evolving a bunch of values. For example, this for loop "evolves" two arrays:
```
for (i, (xs, ys)): (u32, (u16[3], u8[3])) in u32:0..u32:4 {
  ...
}((init_xs, init_ys))
```
Note in the above example arrays are dataflow values just like anything else. To conditionally update an array every other iteration:
```
let result: u4[8] = for (i, array) in u32:0..u32:8 {
  // Update every other cell with the square of the index.
  if i % 2 == 0 { update(array, i, i*i) } else { array }
}(u4[8]:[0, ...]);
```

Numerical Conversions:
DSLX adopts the Rust rules for semantics of numeric casts:

Casting from larger bit-widths to smaller bit-widths will truncate (to the LSbs). * This means that truncating signed values does not preserve the previous value of the sign bit.
Casting from a smaller bit-width to a larger bit-width will zero-extend if the source is unsigned, sign-extend if the source is signed.
Casting from a bit-width to its own bit-width, between signed/unsigned, is a no-op.
```
#[test]
fn test_numerical_conversions() {
  let s8_m2 = s8:-2;
  let u8_m2 = u8:0xfe;
  // Sign extension (source type is signed).
  assert_eq(s32:-2, s8_m2 as s32);
  assert_eq(u32:0xfffffffe, s8_m2 as u32);
  assert_eq(s16:-2, s8_m2 as s16);
  assert_eq(u16:0xfffe, s8_m2 as u16);
  // Zero extension (source type is unsigned).
  assert_eq(u32:0xfe, u8_m2 as u32);
  assert_eq(s32:0xfe, u8_m2 as s32);
  // Nop (bitwidth is unchanged).
  assert_eq(s8:-2, s8_m2 as s8);
  assert_eq(s8:-2, u8_m2 as s8);
  assert_eq(u8:0xfe, u8_m2 as u8);
  assert_eq(s8:-2, u8_m2 as s8);
}
```

Array Conversions:
Casting to an array takes bits from the MSb to the LSb; that is, the group of bits including the MSb ends up as element 0, the next group ends up as element 1, and so on.

Casting from an array to bits performs the inverse operation: element 0 becomes the MSbs of the resulting value.

All casts between arrays and bits must have the same total bit count.
```
fn cast_to_array(x: u6) -> u2[3] {
  x as u2[3]
}

fn cast_from_array(a: u2[3]) -> u6 {
  a as u6
}

fn concat_arrays(a: u2[3], b: u2[3]) -> u2[6] {
  a ++ b
}

#[test]
fn test_cast_to_array() {
  let a_value: u6 = u6:0b011011;
  let a: u2[3] = cast_to_array(a_value);
  let a_array = u2[3]:[1, 2, 3];
  assert_eq(a, a_array);
  // Note: converting back from array to bits gives the original value.
  assert_eq(a_value, cast_from_array(a));

  let b_value: u6 = u6:0b111001;
  let b_array: u2[3] = u2[3]:[3, 2, 1];
  let b: u2[3] = cast_to_array(b_value);
  assert_eq(b, b_array);
  assert_eq(b_value, cast_from_array(b));

  // Concatenation of bits is analogous to concatenation of their converted
  // arrays. That is:
  //
  //  convert(concat(a, b)) == concat(convert(a), convert(b))
  let concat_value: u12 = a_value ++ b_value;
  let concat_array: u2[6] = concat_value as u2[6];
  assert_eq(concat_array, concat_arrays(a_array, b_array));

  // Show a few classic "endianness" example using 8-bit array values.
  let x = u32:0xdeadbeef;
  assert_eq(x as u8[4], u8[4]:[0xde, 0xad, 0xbe, 0xef]);
  let y = u16:0xbeef;
  assert_eq(y as u8[2], u8[2]:[0xbe, 0xef]);
}
```

Bit Slice Expressions:
DSLX supports Python-style bit slicing over unsigned bits types. Note that bits are numbered 0..N starting "from the right (as you would write it on paper)" -- least significant bit, AKA LSb -- for example, for the value `u7:0b100_0111`:
```
    Bit    6 5 4 3 2 1 0
  Value    1 0 0 0 1 1 1
```
A slice expression `[N:M]` means to get from bit `N` (inclusive) to bit `M` exclusive. The start and limit in the slice expression must be signed integral values.

Aside: This can be confusing, because the `N` stands to the left of `M` in the expression, but bit `N` would be to the 'right' of `M` in the classical bit numbering. Additionally, this is not the case in the classical array visualization, where element 0 is usually drawn on the left.

For example, the expression `[0:2]` would yield:
```
    Bit    6 5 4 3 2 1 0
  Value    1 0 0 0 1 1 1
                     ^ ^  included
                   ^      excluded

  Result:  0b11
```
Note that, as of now, the indices for this `[N:M]` form must be literal numbers (so the compiler can determine the width of the result). To perform a slice with a non-literal-number start position, see the `+:` form described below.

The slicing operation also support the python style slices with offsets from start or end. To visualize, one can think of `x[ : -1]` as the equivalent of `x[from the start : bitwidth - 1]`. Correspondingly, `x[-1 : ]` can be visualized as `[ bitwidth - 1 : to the end]`.

For example, to get all bits, except the MSb (from the beginning, until the top element minus 1):
```
x[:-1]
```
Or to get the two most significant bits:
```
x[-2:]
```
This results in the nice property that a the original complete value can be sliced into complementary slices such as `:-2` (all but the two most significant bits) and `-2:` (the two most significant bits):
```
#[test]
fn slice_into_two_pieces() {
  let x = u5:0b11000;
  let (lo, hi): (u3, u2) = (x[:-2], x[-2:]);
  assert_eq(hi, u2:0b11);
  assert_eq(lo, u3:0b000);
}
```
Width Slice:
There is also a "width slice" form `x[start +: bits[N]]` - starting from a specified bit, slice out the next `N` bits. This is equivalent to: `bits[N]:(x >> start)`. The type can be specified as either signed or unsigned; e.g. `[start +: s8]` will produce an 8-bit signed value starting at start, whereas `[start +: u4]` will produce a 4-bit unsigned number starting at `start`.

Here are many more examples:

Bit Slice Examples:
```
// Identity function helper.
fn id<N: u32>(x: bits[N]) -> bits[N] { x }

#[test]
fn test_bit_slice_syntax() {
  let x = u6:0b100111;
  // Slice out two bits.
  assert_eq(u2:0b11, x[0:2]);
  assert_eq(u2:0b11, x[1:3]);
  assert_eq(u2:0b01, x[2:4]);
  assert_eq(u2:0b00, x[3:5]);

  // Slice out three bits.
  assert_eq(u3:0b111, x[0:3]);
  assert_eq(u3:0b011, x[1:4]);
  assert_eq(u3:0b001, x[2:5]);
  assert_eq(u3:0b100, x[3:6]);

  // Slice out from the end.
  assert_eq(u1:0b1, x[-1:]);
  assert_eq(u1:0b1, x[-1:6]);
  assert_eq(u2:0b10, x[-2:]);
  assert_eq(u2:0b10, x[-2:6]);
  assert_eq(u3:0b100, x[-3:]);
  assert_eq(u3:0b100, x[-3:6]);
  assert_eq(u4:0b1001, x[-4:]);
  assert_eq(u4:0b1001, x[-4:6]);

  // Slice both relative to the end (MSb).
  assert_eq(u2:0b01, x[-4:-2]);
  assert_eq(u2:0b11, x[-6:-4]);

  // Slice out from the beginning (LSb).
  assert_eq(u5:0b00111, x[:-1]);
  assert_eq(u4:0b0111, x[:-2]);
  assert_eq(u3:0b111, x[:-3]);
  assert_eq(u2:0b11, x[:-4]);
  assert_eq(u1:0b1, x[:-5]);

  // Slicing past the end just means we hit the end (as in Python).
  assert_eq(u1:0b1, x[5:7]);
  assert_eq(u1:0b1, x[-7:1]);
  assert_eq(bits[0]:0, x[-7:-6]);
  assert_eq(bits[0]:0, x[-6:-6]);
  assert_eq(bits[0]:0, x[6:6]);
  assert_eq(bits[0]:0, x[6:7]);
  assert_eq(u1:1, x[-6:-5]);

  // Slice of a slice.
  assert_eq(u2:0b11, x[:4][1:3]);

  // Slice of an invocation.
  assert_eq(u2:0b01, id(x)[2:4]);

  // Explicit-width slices.
  assert_eq(u2:0b01, x[2+:u2]);
  assert_eq(s3:0b100, x[3+:s3]);
  assert_eq(u3:0b001, x[5+:u3]);
}
```

Advanced Understanding: Parametricity, Constraints, and Unification:
An infamous wrinkle is introduced for parametric functions: consider the following function:
```
// (Note: DSLX does not currently support the `T: type` construct shown here,
// it is for example purposes only.)
fn add_wrapper<T: type, U: type>(x: T, y: U) -> T {
  x + y
}
```
Based on the inference rule, we know that '+' can only type check when the operand types are the same. This means we can conclude that type `T` is the same as type `U`. Once we determine this, we need to make sure anywhere `U` is used it is consistent with the fact it is the same as `T`. In a sense the + operator is "adding a constraint" that `T` is equivalent to `U`, and trying to check that fact is valid is under the purview of type inference. The fact that the constraint is added that `T` and `U` are the same type is referred to as "unification", as what was previously two entities with potentially different constraints now has a single set of constraints that comes from the union of its operand types.

DSLX's typechecker will go through the body of parametric functions per invocation. As such, the typechecker will always have the invocation's parametric values for use in asserting type consistency against "constraints" such as derived parametric expressions, body vs. annotated return type equality, and expression inference rules.

Operator Precedence:
DSLX's operator precedence matches Rust's. Listed below are DSLX's operators in descending precedence order. Binary operators at the same level share the same associativity and will be grouped accordingly.

Operator	    			Associativity
Unary `-` `!`   			n/a
`as`            			Left to right
`*` `/` `%`     			Left to right
`+` `-`	            		Left to right
`<<` `>>` `>>>`	    		Left to right
`&`	            			Left to right
`^`	            			Left to right
`\|`	            		Left to right
`==` `!=` `<` `>` `<=` `>=`	Left to right
`&&`	            		Left to right
`\|\|`	        			Left to right
