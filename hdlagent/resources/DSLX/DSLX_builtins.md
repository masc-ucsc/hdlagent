**User:** Builtins:
This section describes the built-in functions provided for use in the DSL that do not need to be explicitly imported.

A note on "Parallel Primitives": the DSL is expected to grow additional support for use of high-level parallel primitives over time, adding operators for order-insensitive reductions, scans, groupings, and similar. By making these operations known to the compiler in their high level form, we potentially enable optimizations and analyses on their higher level ("lifted") form. As of now, `map` is the sole parallel-primitive-oriented built-in.

`add_with_carry` :
Operation that produces the result of the add, as well as the carry bit as an output. The binary add operators works similar to software programming languages, preserving the length of the input operands, so this builtin can assist when easy access to the carry out value is desired. Has the following signature:
```
fn add_with_carry<N>(x: uN[N], y: uN[N]) -> (u1, uN[N])
```
`widening_cast` and `checked_cast`
`widening_cast` and `checked_cast` cast bits-type values to bits-type values with additional checks compared to casting with `as`.

`widening_cast` will report a static error if the type casted to is unable to respresent all values of the type casted from (ex. `widening_cast<u5>(s3:0)` will fail because s3:-1 cannot be respresented as an unsigned number).

`checked_cast` will cause a runtime error during dslx interpretation if the value being casted is unable to fit within the type casted to (ex. `checked_cast<u5>(s3:0)` will succeed while `checked_cast<u5>(s3:-1)` will cause the dslx interpreter to fail.

Currently both `widening_cast` and `checked_cast` will lower into a normal IR cast and will not generate additional assertions at the IR or Verilog level.
```
fn widening_cast<sN[N]>(value: uN[M]) -> sN[N]; where N > M
fn widening_cast<sN[N]>(value: sN[M]) -> sN[N]; where N >= M
fn widening_cast<uN[N]>(value: uN[M]) -> uN[N]; where N >= M

fn checked_cast<xN[M]>(value: uN[N]) -> xN[M]
fn checked_cast<xN[M]>(value: sN[N]) -> xN[M]
```

`smulp` and `umulp`:
`smulp` and `umulp` perform signed and unsigned partial multiplications. These operations return a two-element tuple with the property that the sum of the two elements is equal to the product of the original inputs. Performing a partial multiplication allows for a pipeline stage in the middle of a multiply. These operations have the following signatures:
```
fn smulp<N>(lhs: sN[N], rhs: sN[N]) -> (sN[N], sN[N])
fn umulp<N>(lhs: uN[N], rhs: uN[N]) -> (uN[N], uN[N])
```

`map`:
`map`, similarly to other languages, executes a transformation function on all the elements of an original array to produce the resulting "mapped' array. For example: taking the absolute value of each element in an input array:
```
import std

fn main(x: s3[3]) -> s3[3] {
  let y: s3[3] = map(x, std::abs);
  y
}

#[test]
fn main_test() {
  let got: s3[3] = main(s3[3]:[-1, 1, 0]);
  assert_eq(s3[3]:[1, 1, 0], got)
}
```
Note that map is special, in that we can pass it a callee as if it were a value. As a function that "takes" a function as an argument, `map` is a special builtin -- in language implementor parlance it is a higher order function.

Implementation note: Functions are not first class values in the DSL, so the name of the function must be referred to directly.

Note: Novel higher order functions (e.g. if a user wanted to write their own `map`) cannot currently be written in user-level DSL code.

`array_rev`:
`array_rev` reverses the elements of an array.
```
#[test]
fn test_array_rev() {
  assert_eq(array_rev(u8[1]:[42]), u8[1]:[42]);
  assert_eq(array_rev(u3[2]:[1, 2]), u3[2]:[2, 1]);
  assert_eq(array_rev(u3[3]:[2, 3, 4]), u3[3]:[4, 3, 2]);
  assert_eq(array_rev(u4[3]:[0xf, 0, 0]), u4[3]:[0, 0, 0xf]);
  assert_eq(array_rev(u3[0]:[]), u3[0]:[]);
}
```
`clz`, `ctz`:
DSLX provides the common "count leading zeroes" and "count trailing zeroes" functions:
```
  let x0 = u32:0x0FFFFFF8;
  let x1 = clz(x0);
  let x2 = ctz(x0);
  assert_eq(u32:4, x1);
  assert_eq(u32:3, x2)
```

`one_hot`:

Converts a value to one-hot form. Has the following signature:
```
fn one_hot<N, NP1=N+1>(x: uN[N], lsb_is_prio: bool) -> uN[NP1]
```
When `lsb_is_prio` is true, the least significant bit that is set becomes the one-hot bit in the result. When it is false, the most significant bit that is set becomes the one-hot bit in the result.

When all bits in the input are unset, the additional bit present in the output value (MSb) becomes set.

signex:
Casting has well-defined extension rules, but in some cases it is necessary to be explicit about sign-extensions, if just for code readability. For this, there is the `signex` builtin.

To invoke the `signex` builtin, provide it with the operand to sign extend (lhs), as well as the target type to extend to: these operands may be either signed or unsigned. Note that the value of the right hand side is ignored, only its type is used to determine the result type of the sign extension.
```
#[test]
fn test_signex() {
  let x = u8:0xff;
  let s: s32 = signex(x, s32:0);
  let u: u32 = signex(x, u32:0);
  assert_eq(s as u32, u)
}
```
Note that both `s` and `u` contain the same bits in the above example.

slice:
Array-slice builtin operation. Note that the "want" argument is not used as a value, but is just used to reflect the desired slice type. (Prior to constexprs being passed to builtin functions, this was the canonical way to reflect a constexpr in the type system.) Has the following signature:
```
fn slice<T: type, N, M, S>(xs: T[N], start: uN[M], want: T[S]) -> T[S]
```
rev:
`rev` is used to reverse the bits in an unsigned bits value. The LSb in the input becomes the MSb in the result, the 2nd LSb becomes the 2nd MSb in the result, and so on.
```
// (Dummy) wrapper around reverse.
fn wrapper<N: u32>(x: bits[N]) -> bits[N] {
  rev(x)
}

// Target for IR conversion that works on u3s.
fn main(x: u3) -> u3 {
  wrapper(x)
}

// Reverse examples.
#[test]
fn test_reverse() {
  assert_eq(u3:0b100, main(u3:0b001));
  assert_eq(u3:0b001, main(u3:0b100));
  assert_eq(bits[0]:0, rev(bits[0]:0));
  assert_eq(u1:1, rev(u1:1));
  assert_eq(u2:0b10, rev(u2:0b01));
  assert_eq(u2:0b00, rev(u2:0b00));
}
```
`bit_slice_update`:
`bit_slice_update(subject, start, value)` returns a copy of the bits-typed value `subject` where the contiguous bits starting at index `start` (where 0 is the least-significant bit) are replaced with `value`. The bit-width of the returned value is the same as the bit-width of `subject`. Any updated bit indices which are out of bounds (if `start + bit-width(value) >= bit-width(subject)`) are ignored.

Bitwise reduction builtins: and_reduce, or_reduce, xor_reduce:
These are unary reduction operations applied to a bits-typed value:

`and_reduce`: evaluates to bool:1 if all bits of the input are set, and 0 otherwise.
`or_reduce`: evaluates to bool:1 if any bit of the input is set, and 0 otherwise.
`xor_reduce`: evaluates to bool:1 if there is an odd number of bits set in the input, and 0 otherwise.
These functions return the identity element of the respective operation for trivial (0 bit wide) inputs:
```
#[test]
fn test_trivial_reduce() {
  assert_eq(and_reduce(bits[0]:0), true);
  assert_eq(or_reduce(bits[0]:0), false);
  assert_eq(xor_reduce(bits[0]:0), false);
}
```

update:
`update(array, index, new_value)` returns a copy of `array` where `array[index]` has been replaced with `new_value`, and all other elements are unchanged. Note that this is not an in-place update of the array, it is an "evolution" of `array`. It is the compiler's responsibility to optimize by using mutation instead of copying, when it's safe to do. The compiler makes a best effort to do this, but can't guarantee the optimization is always made.

`assert_eq`, `assert_lt`:
In a unit test pseudo function all valid DSLX code is allowed. To evaluate test results DSLX provides the `assert_eq` primitive (we'll add more of those in the future). Here is an example of a `divceil` implementation with its corresponding tests:
```
fn divceil(x: u32, y: u32) -> u32 {
  (x-u32:1) / y + u32:1
}

#[test]
fn test_divceil() {
  assert_eq(u32:3, divceil(u32:5, u32:2));
  assert_eq(u32:2, divceil(u32:4, u32:2));
  assert_eq(u32:2, divceil(u32:3, u32:2));
  assert_eq(u32:1, divceil(u32:2, u32:2));
}
```
`assert_eq` cannot currently be synthesized into equivalent Verilog. Because of that it is recommended to use it within `test` constructs (interpretation) only.

`zero!<T>`:
DSLX has a macro for easy creation of zero values, even from aggregate types. Invoke the macro with the type parameter as follows:
```
struct MyPoint {
  x: u32,
  y: u32,
}

enum MyEnum : u2 {
  ZERO = u2:0,
  ONE = u2:1,
}

#[test]
fn test_zero_macro() {
  assert_eq(zero!<u32>(), u32:0);
  assert_eq(zero!<MyPoint>(), MyPoint{x: u32:0, y: u32:0});
  assert_eq(zero!<MyEnum>(), MyEnum::ZERO);
}
```
The `zero!<T>` macro can also be used with the struct update syntax to initialize a subset of fields to zero. In the example below all fields except `foo` are initialized to zero in the struct returned by `f`.
```
struct MyStruct {
  foo: u1,
  bar: u2,
  baz: u3,
  bat: u4,
}

fn f() -> MyStruct {
  MyStruct{foo: u1:1, ..zero!<MyStruct>()}
}
```
