## **DSLX Syntax Differences with Other HDLs**

**1. Parametric types and functions:** DSLX supports parametric types and functions, which allow you to
 write code that can work on data of different formats and layouts.

```dslx
pub fn umax<N: u32>(x: uN[N], y: uN[N]) -> uN[N] {
  if x > y { x } else { y }
}
```

This function calculates the maximum of two numbers of any specified type `N`, where `N` is a parametric value.

**2.
 `for` expressions:** DSLX provides a `for` construct for iterating through a fixed number of times.

```dslx
for (i, crc): (u32, u32) in range(u32:8) {
  // Loop body
}
```

This
 loop iterates 8 times, with `i` being the loop index and `crc` being an accumulator variable.

**3. Tuple return values:** DSLX functions can return multiple values as a tuple.

```dslx
pub fn get_values() -> (u32, u64) {
  (u32:42, u64:1024)
}
```

This function returns a tuple containing a
 32-bit integer and a 64-bit integer.

**4. Automatic type inference:** DSLX has a powerful type inference engine that can automatically determine the types of variables and expressions.

```dslx
let x = 42;  // Automatically inferred as u32
let y = x + 10;  // Automatically inferred as u32
```

This allows you to write code without explicitly specifying types everywhere.


**5. constexpr-style evaluation:** DSLX supports constexpr-style evaluation, which allows you to evaluate constant expressions at interpretation or compilation time.

```dslx
let bias_scaler = (sN[WIDE_N]:1 << (N - u32:1)) - sN[WIDE_N]:1;
```

This expression calculates a constant value that can be used in other parts of the code.

**6. DSLX syntax is intended to follow Rust syntax as much as possible.**

**7. DSLX has a full details on language features and syntax in the DSLX language reference.**


**8. DSLX is still under development, and its syntax may change in the future.**

**9. DSLX is an open-source language, and its development is managed on GitHub.**

**10. DSLX has a growing community of users.**
