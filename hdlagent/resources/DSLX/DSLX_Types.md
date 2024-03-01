**User:** Types:

Bit Type:
The most fundamental type in DSLX is a variable length bit type denoted as `bits[n]`, where `n` is a constant. For example:
```
bits[1]   // a single bit
uN[1]     // explicitly noting single bit is unsigned
u1        // convenient shorthand for bits[1]

bits[8]   // an 8-bit datatype, yes, a byte
u8        // convenient shorthand for bits[8]
bits[32]  // a 32-bit datatype
u32       // convenient shorthand for bits[32]
bits[256] // a 256-bit datatype

bits[0]   // possible, but, don't do that
```
DSLX introduces aliases for commonly used types, such as `u8` for an 8-wide bit type, or `u32` for a 32-bit wide bit type. These are defined up to `u64`.
All `u*`, `uN[*]`, and `bits[*]` types are interpreted as unsigned integers. Signed integers are specified via `s*` and `sN[*]`. Similarly to unsigned numbers, the `s*` shorthands are defined up to `s64`. For example:
```
sN[1]
s1

sN[64]
s64

sN[256]

sN[0]
s0
```
Signed numbers differ in their behavior from unsigned numbers primarily via operations like comparisons, (variable width) multiplications, and divisions.
Bit Type Attributes:
Bit types have helpful type-level attributes that provide limit values, similar to `std::numeric_limits` in C++. For example:
```
u3::MAX   // u3:0b111 the "fill with ones" value
s3::MAX   // s3:0b011 the "maximum signed" value

u3::ZERO  // u3:0b000 the "fill with zeros" value
s3::ZERO  // s3:0b000 the "fill with zeros" value
```
Character Constants:
Characters are a special case of bits types: they are implicitly-type as u8. Characters can be used just as traditional bits:
```
fn add_to_null(input: u8) -> u8 {
  let null:u8 = '\0';
  input + null
}

#[test]
fn test_main() {
  assert_eq('a', add_to_null('a'))
}
```
DSLX character constants support the full Rust set of escape sequences with the exception of unicode.
Enum Types:
DSLX supports enumerations as a way of defining a group of related, scoped, named constants that do not pollute the module namespace. For example:
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
Note the use of the double-colon to reference the enum value. This code specifies that the enum behaves like a `u3:` its storage and extension (via casting) behavior are defined to be those of a `u3`. Attempts to define an enum value outside of the representable `u3` range will produce a compile time error.
```
enum Opcode : u3 {
  FOO = 8  // Causes compile time error!
}
```
Enums can be compared for equality/inequality, but they do not permit arithmetic operations, they must be cast to numerical types in order to perform arithmetic:
```
enum Opcode: u3 {
  NOP = 0,
  ADD = 1,
  SUB = 2,
  MUL = 3,
}

fn same_opcode(x: Opcode, y: Opcode) -> bool {
  x == y  // ok
}

fn next_in_sequence(x: Opcode, y: Opcode) -> bool {
  // x+1 == y // does not work, arithmetic!
  x as u3 + u3:1 == (y as u3)  // ok, casted first
}
```
As mentioned above, casting of enum-values works with the same casting/extension rules that apply to the underlying enum type definition. For example, this cast will sign extend because the source type for the enum is signed.
```
enum MySignedEnum : s3 {
  LOW = -1,
  ZERO = 0,
  HIGH = 1,
}

fn extend_to_32b(x: MySignedEnum) -> u32 {
  x as u32  // Sign-extends because the source type is signed.
}

#[test]
fn test_extend_to_32b() {
  assert_eq(extend_to_32b(MySignedEnum::LOW), u32:0xffffffff)
}
```
Casting to an enum is also permitted. However, in most cases errors from invalid casting can only be found at runtime, e.g., in the DSL interpreter or flagging a fatal error from hardware. Because of that, it is recommended to avoid such casts as much as possible.
Tuple Type:
A tuple is a fixed-size ordered set, containing elements of heterogeneous types. Tuples elements can be any type, e.g. bits, arrays, structs, tuples. Tuples may be empty (an empty tuple is also known as the unit type), or contain one or more types.

Examples of tuple values:
```
// The unit type, carries no information.
let unit = ();

// A tuple containing two bits-typed elements.
let pair = (u3:0b100, u4:0b1101);
```
Example of a tuple type:
```
// The type of a tuple with 2 elements.
//   the 1st element is of type u32
//   the 2nd element is a tuple with 3 elements
//       the 1st element is of type u8
//       the 2nd element is another tuple with 1 element of type u16
//       the 3rd element is of type u8
type MyTuple = (u32, (u8, (u16,), u8));
```
To access individual tuple elements use simple indices, starting at 0. For example, to access the second element of a tuple (index 1):
```
#[test]
fn test_tuple_access() {
  let t = (u32:2, u8:3);
  assert_eq(u8:3, t.1)
}
```
Such indices can only be numeric literals; parametric symbols are not allowed.

Tuples can be "destructured", similarly to how pattern matching works in `match` expressions, which provides a convenient syntax to name elements of a tuple for subsequent use. See `a` and `b` in the following:
```
#[test]
fn test_tuple_destructure() {
  let t = (u32:2, u8:3);
  let (a, b) = t;
  assert_eq(u32:2, a);
  assert_eq(u8:3, b)
}
```
Just as values can be discarded in a `let` by using the "black hole identifier" `_`, don't-care values can also be discarded when destructuring a tuple:
```
#[test]
fn test_black_hole() {
  let t = (u32:2, u8:3, true);
  let (_, _, v) = t;
  assert_eq(v, true)
}
```
Struct Types:
Structures are similar to tuples, but provide two additional capabilities: we name the slots (i.e. struct fields have names while tuple elements only have positions), and we introduce a new type.

The following syntax is used to define a struct:
```
struct Point {
  x: u32,
  y: u32
}
```
Once a struct is defined it can be constructed by naming the fields in any order:
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
There is a simple syntax when creating a struct whose field names match the names of in-scope values
```
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
```
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
Note that structs cannot be mutated "in place", the user must construct new values by extracting the fields of the original struct mixed together with new field values, as in the following:
```
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

Struct Update Syntax:
The DSL has syntax for conveniently producing a new value with a subset of fields updated to reduce verbosity. The "struct update" syntax is:
```
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
Parametric Structs:
DSLX also supports parametric structs.
```
fn double(n: u32) -> u32 { n * u32:2 }

struct Point<N: u32, M: u32 = {double(N)}> {
  x: bits[N],
  y: bits[M],
}

fn make_point<A: u32, B: u32>(x: bits[A], y: bits[B]) -> Point<A, B> {
  Point{ x, y }
}

#[test]
fn test_struct_construction() {
  let p = make_point(u16:42, u32:42);
  assert_eq(u16:42, p.x)
}
```
Understanding Nominal Typing:
As mentioned above, a struct definition introduces a new type. Structs are nominally typed, as opposed to structurally typed (note that tuples are structurally typed). This means that structs with different names have different types, regardless of whether those structs have the same structure (i.e. even when all the fields of two structures are identical, those structures are a different type when they have a different name).
```
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

```
#[test]
fn test_type_checker_error() {
  assert_eq(f(Coordinate { x: u32:42, y: u32:64 }), u32:106)
}
```
Array Type:
Arrays can be constructed via bracket notation. All values that make up the array must have the same type. Arrays can be indexed with indexing notation (`a[i]`) to retrieve a single element.
```
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
Because arrays with repeated trailing elements are common, the DSL supports ellipsis (`...`) at the end of an array to fill the remainder of the array with the last noted element. Because the compiler must know how many elements to fill, in order to use the ellipsis the type must be annotated explicitly as shown.
```
fn make_array(x: u32) -> u32[3] {
  u32[3]:[u32:42, x, ...]
}

#[test]
fn test_make_array() {
  assert_eq(u32[3]:[u32:42, u32:42, u32:42], make_array(u32:42));
  assert_eq(u32[3]:[u32:42, u32:64, u32:64], make_array(u32:64));
}
```
Note google/xls#917: arrays with length zero will typecheck, but fail to work in most circumstances. Eventually, XLS should support them but they can't be used currently.

Character String Constants:
Character strings are a special case of array types, being implicitly-sized arrays of u8 elements. String constants can be used just as traditional arrays:
```
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
DSLX string constants support the full Rust set of escape sequences - note that unicode escapes get encoded to their UTF-8 byte sequence. In other words, the sequence `\u{10CB2F}` will result in an array with hexadecimal values `F4 8C AC AF`.

Moreover, string can be composed of characters.
```
fn string_composed_characters() -> u8[10] {
  ['X', 'L', 'S', ' ', 'r', 'o', 'c', 'k', 's', '!']
}
}

#[test]
fn test_main() {
  assert_eq("XLS rocks!", string_composed_characters())
}
```
