# DSLX Syntax Guide for LLMs: Top 10 Differences from Other HDLs

DSLX is a Hardware Description Language (HDL) designed with unique syntax and features that distinguish it from other HDLs like Verilog or VHDL. This guide highlights the top 10 syntax differences, providing code snippets for each to aid LLMs in generating DSLX code effectively.

## 1. Function Definition

DSLX uses Rust-like syntax for function definition, emphasizing clarity and type safety.

### DSLX
```dslx
pub fn float_to_int(x: float32) -> s32 {
  // Function body
}
```

### Other HDLs
```verilog
function integer float_to_int(input float32 x);
  // Function body
endfunction
```

## 2. Data Types and Type Aliases

DSLX introduces concise type declarations and aliases, streamlining the definition of complex types.

### DSLX
```dslx
pub struct float32 {
  sign: u1,
  bexp: u8,
  fraction: u23,
}
```

### Other HDLs
```verilog
typedef struct {
  bit sign;
  bit [7:0] bexp;
  bit [22:0] fraction;
} float32;
```

## 3. Tuple Types

DSLX allows packing disparate elements into a single tuple type, a feature not commonly found in traditional HDLs.

### DSLX
```dslx
(x: (u1, u8, u23)) -> s32
```

### Other HDLs
Typically, HDLs like Verilog or VHDL do not have direct tuple support and would require either multiple arguments or a custom struct.

## 4. Parametric Functions

DSLX supports parametric functions, enabling more generic and reusable code.

### DSLX
```dslx
pub fn umax<N: u32>(x: uN[N], y: uN[N]) -> uN[N] {
  if x > y { x } else { y }
}
```

### Other HDLs
Generic functions in other HDLs often require more verbose and less intuitive syntax.

## 5. For Expressions

DSLX introduces `for` expressions for iterating a fixed number of times, a powerful construct for describing hardware loops.

### DSLX
```dslx
for (i, crc): (u32, u32) in range(u32:8) {
  // Loop body
}(crc)
```

### Other HDLs
Other HDLs use traditional for-loop constructs which may not directly translate to hardware loops.

## 6. Type Inference

DSLX aims to reduce redundancy through type inference, though it's still a work in progress.

### DSLX
```dslx
let result = if x.sign { -result } else { result };
```

### Other HDLs
Explicit type declarations are often required, increasing verbosity.

## 7. Constants and Literals

DSLX uses a Rust-like syntax for constants and literals, emphasizing readability.

### DSLX
```dslx
let fraction = u33:1 << 23 | (x.fraction as u33);
```

### Other HDLs
```verilog
assign fraction = {1'b1, x.fraction};
```

## 8. Structs for Data Packing

DSLX utilizes structs for packing data, similar to C structs, but with more concise syntax.

### DSLX
```dslx
pub struct float32 {
  sign: u1,
  bexp: u8,
  fraction: u23,
}
```

### Other HDLs
Data packing in other HDLs often requires separate declarations or arrays.

## 9. Implicit Leading One in Floating-Point Numbers

DSLX code explicitly handles the implicit leading one in floating-point numbers, a detail often abstracted away in other HDLs.

### DSLX
```dslx
let fraction = u33:1 << 23 | (x.fraction as u33);
```

### Other HDLs
Handling of the implicit leading one is usually implicit in the floating-point operations themselves.

## 10. Signed and Unsigned Type Declarations

DSLX provides clear distinctions between signed and unsigned types, enhancing type safety.

### DSLX
```dslx
fn unbias_exponent(exp: u8) -> s9 {
  exp as s9 - s9:127
}
```

### Other HDLs
Type distinctions are present but may not be as emphasized or clear in syntax.

This guide aims to provide a foundational understanding of DSLX's unique syntax features. By leveraging these differences, LLMs can generate DSLX code more effectively, contributing to the development of hardware designs with clarity and precision.
