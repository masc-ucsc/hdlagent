# DSLX Language Essentials for LLMs

DSLX is a Hardware Description Language designed to facilitate the creation of hardware modules, including those for floating-point arithmetic and parametric types. This documentation provides a concise overview of DSLX syntax and key features, tailored for Language Learning Models (LLMs) generating DSLX code. It includes code snippets and explanations of language syntax to highlight DSLX's unique aspects.

## Basic Logic and Data Types

DSLX syntax is inspired by Rust, aiming for familiarity to those with experience in Rust programming. Here's a quick look at defining functions, tuples, and structs:

### Function Definition

```dslx
pub fn float_to_int(x: (u1, u8, u23)) -> s32 {
  // Function body
}
```

- `pub fn` declares a public function.
- Parameters are defined with their types following their names, e.g., `x: (u1, u8, u23)` where `x` is a tuple.
- Return type is specified after the `->`, e.g., `s32` for a signed 32-bit integer.

### Struct Definition

```dslx
pub struct float32 {
  sign: u1,
  bexp: u8,
  fraction: u23,
}
```

- Structs group related data, similar to structs in C or Rust.
- Fields are declared with their types, e.g., `sign: u1` for a 1-bit unsigned integer.

## Simple Logic Implementation

Implementing logic involves manipulating data based on the defined types. For example, to unbias an exponent:

```dslx
fn unbias_exponent(exp: u8) -> s9 {
  exp as s9 - s9:127
}
```

- Type casting and arithmetic operations are straightforward, e.g., `exp as s9` casts `exp` to a 9-bit signed integer.

## Parametric Types and Functions

DSLX supports parametric types and functions, allowing for more generic and reusable code.

### Parametric Function Example

```dslx
pub fn umax<N: u32>(x: uN[N], y: uN[N]) -> uN[N] {
  if x > y { x } else { y }
}
```

- `<N: u32>` declares a parametric value, making the function applicable to types of various sizes.
- `uN[N]` uses the parametric value `N` to define the width of the input and output types.

### Derived Parametrics and Constants

DSLX allows for derived parametric values and supports compile-time constant expressions:

```dslx
fn bias_scaler<N: u32, WIDE_N: u32 = {N + u32:1}>() -> sN[WIDE_N] {
  (sN[WIDE_N]:1 << (N - u32:1)) - sN[WIDE_N]:1
}
```

- `{N + u32:1}` defines a derived parametric value.
- Compile-time constant expressions enable calculations based on parametric values.

## `for` Expressions

DSLX includes `for` expressions for iterating a fixed number of times, useful for implementing algorithms like CRC32 checksums.

### `for` Loop Structure

```dslx
for (i, crc): (u32, u32) in range(u32:8) {
  // Loop body
}(crc)
```

- Iterates 8 times, with `i` as the index and `crc` as the accumulator.
- The loop body's last expression determines the next iteration's accumulator value or the final result.

## Conclusion

This documentation provides a snapshot of DSLX's syntax and features, focusing on aspects that distinguish it from other languages. By understanding these basics, LLMs can generate DSLX code more effectively, contributing to hardware design and simulation tasks.
