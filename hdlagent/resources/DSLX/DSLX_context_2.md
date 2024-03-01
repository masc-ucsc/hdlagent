**User:** I have a new HDL programming language called DSLX that resembles a modern language like **rust** but it has the following key differences:

* Support multiple bit sizes `fn call(a:bits[3])` is the same as `fn call(a:u3)`

* Bit types can have attributes like `u3::MAX == 0b111`

* u8 is a character `let null:u8 = '\0';`

* The tuple type is an ordered set `let pair = (u3:0b100, u4:0b1101);`

* The array type uses bracket notation. E.g: `let my_array: u32[2] = [0,3];`

* Bit slicing is similiar to Python indexing and string slicing. E.g: `let (lo, hi): (u3, u2) = (x[:-2], x[-2:]);`

* Bit slicing also allows a delta similar to Verliog, but the second field is a type. E.g `let lower_4bits = x[0+:u4]`

* assert_eq does not need the ! for macro

* type casting allows to convert across bitwidths. E.g: `assert((u4:0b1100) as u2 == u2:0)`

* Structs and tuples have by default a `PartialEq` implementation.

* DSLX only supports “implicit return”. This means that the final expression in a function will automatically be used as the return value if no explicit return statement is given.

* DSLX only supports assert_eq for testing

* In DSLX the Return type of function body has to match the annotated return type.

* `carry` is a keyword, form naming, use specific naming to avoid confusion with keywords. It's important to choose variable names that are descriptive and meaningful, avoiding those that coincide with reserved keywords


Some sample code:

```
#[test]
fn test_tuple_access() {
  let t = (u32:2, u8:3);
  assert_eq(u8:3, t.1)
}
```

```
#[test]
fn test_black_hole() {
  let t = (u32:2, u8:3, true);
  let (_, _, v) = t;
  assert_eq(v, true)
}
```

```
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

```
_Ok123_321        // valid identifier
_                 // valid identifier

2ab               // not valid identifier
&ade              // not valid identifier
```

```
fn ret3() -> u32 {
   u32:3   // This function always returns 3.
}

fn add1(x: u32) -> u32 {
   x + u32:1  // Returns x + 1, but you knew that!
}
```

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

```
//Parametric Functions
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

```
enum Opcode : u3 {
  FIRE_THE_MISSILES = 0,
  BE_TIRED = 1,
  TAKE_A_NAP = 2,
}

fn get_my_favorite_opcode() -> Opcode {
  Opcode::FIRE_THE_MISSILES
}
```

```
// The unit type, carries no information.
let unit = ();

// A tuple containing two bits-typed elements.
let pair = (u3:0b100, u4:0b1101);
```

```#[test]
fn test_tuple_access() {
  let t = (u32:2, u8:3);
  assert_eq(u8:3, t.1)
}
```

This example returns the bit 6 after adding two numbers with different widths
```
fn pic6_from_add(ss: u4, xx:u8) -> u1 {
  let result = ss as u8 + xx;
  result[6+:u1]
}
```

The following example picks 0 if ss matches xx, or the 4 bits from 3 to 7 out of b otherwise:
```
fn pick_weird(ss: u4, b:u8, xx: u1) -> u4 {
  if (ss == xx as u4) {
    u4:0
  }else{
    b[3+:u4]
  }
}
```

DSLX supports compile loops, but the syntax is different from Rust. It has an
accumulator across iterations.


This example add up values from 7 to 11 (exclusive) in a 16 bit output:

```
struct Outputs {
  result: u16,
}

fn add_7_to_11() -> Outputs {

  //To add up values from 7 to 11 (exclusive), one would write:

  let base = u16:7;
  let res = for (i, accum): (u16, u16) in u16:0..u16:4 {
    accum + base + i
  }(u16:0);

  Outputs { result: res }
}
```
