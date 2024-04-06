**DSLX Tutorial
 for LLMs**

**Section 1: Introduction**

DSLX is a Hardware Description Language with unique features that make it suitable for
 generating code. This documentation aims to provide a comprehensive guide for LLMs trying to generate DSLX code.

**Section 2:
 Basic Syntax**

**2.1: Data Types**

- **Unsigned integers**: `uN[X]`, where X is the bit width (e.g., `u8`)
- **
Signed integers**: `sN[X]`, where X is the bit width (e.g., `s32`)
- **Tuples**: Parentheses containing multiple types (e.g., `(u8, u16)`)

**2.2
: Functions**

- **Function declaration**: `pub fn <function_name>(<parameters>) -> <return_type>`
- **Parameter**: `<parameter_name>: <type>`
- **Return type**: `<type>` (e.g., `s32`)
- **Function body**: Enclosed in curly braces ({})


**Section 3: Parametric Types and Functions**

**3.1: Parametric Types**

- **Parametric type**: `<type_name>: <parameter>`
- **Parameter**: Specifies the type's size or layout
- **Example**: `float<EXP_SZ: u32, FRACTION_SZ: u32>`

**3.2:
 Parametric Functions**

- **Parametric function**: `pub fn <function_name><<parameters>>(<parameters>) -> <return_type>`
- **Parameters**: Can specify parametric values (e.g., `N`)
- **Parametric values**: `<type_name>: <value>`
- **Example**: `umax<N: u32>(x: <type>, y: <type>) -> <type>`

**Section 4: For Expressions**

**
4.1: Syntax**

- `for (<index>, <accumulators>): (<index_type>, <accumulator_types>) in <iterable>`
- **Index**: Loop counter
- **Accumulators**: Variables that carry data between iterations
- **Iterable**: `range(u32:8)` or `enumerate()`

**4.2: Loop Body**

- Enclosed in curly braces ({})
-
 Last expression is assigned to the accumulators

**Example:**

```dslx
for (i, crc): (u32, u32) in range(u32:8) {
  let mask: u32 = -(crc & u32:1);
  (crc >> u32:1) ^ (polynomial & mask)
}
```

**Section 5: Code Snippets**

**5.1: Float-to-Integer Conversion**

```dslx
pub struct float<EXP_SZ: u32
, FRACTION_SZ: u32> {
  sign: u1,
  bexp: uN[EXP_SZ],
  fraction: uN[FRACTION_SZ],
}

pub fn float_to_int<
    EXP_SZ: u32, FRACTION_SZ: u32, RESULT_SZ: u32,
    WIDE_EXP_SZ: u32 = {EXP_SZ + u32:1},
    WIDE_FRACTION_SZ: u32 = {FRACTION_SZ + u32:1}>(

    x: float<EXP_SZ, FRACTION_SZ>) -> sN[RESULT_SZ] {
  ...
}
```

**5.2: CRC32 One-Byte Update**

```dslx
fn crc32_one_byte_update(previous_crc: u32, byte: u8) -> u32 {
  let polynomial: u32 = ...;  // Polynomial representing CRC32-C

  // 8 rounds of updates.
  for (i, crc): (u32, u32) in range(u3
2:8) {
    let mask: u32 = -(crc & u32:1);
    (crc >> u32:1) ^ (polynomial & mask)
  }(previous_crc)
}
```
