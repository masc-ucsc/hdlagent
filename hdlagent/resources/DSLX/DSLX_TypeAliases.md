**User:** Type Aliases:
DLSX supports the definition of type aliases.

Type aliases can be used to provide a more human-readable name for an existing type. The new name is on the left, the existing name on the right:
```
type Weight = u6;
```
We can create an alias for an imported type:
```
// Note: this imports an external file in the codebase.
import xls.dslx.tests.mod_imported

type MyEnum = mod_imported::MyEnum;

fn main(x: u8) -> MyEnum {
  x as MyEnum
}

#[test]
fn test_main() {
  assert_eq(main(u8:42), MyEnum::FOO);
  assert_eq(main(u8:64), MyEnum::BAR);
}
```
Type aliases can also provide a descriptive name for a tuple type (which is otherwise anonymous). For example, to define a tuple type that represents a float number with a sign bit, an 8-bit mantissa, and a 23-bit mantissa, one would write:
```
type F32 = (u1, u8, u23);
```
After this definition, the `F32` may be used as a type annotation interchangeably with `(u1, u8, u23)`.

Note, however, that structs are generally preferred for this purpose, as they are more readable and users do not need to rely on tuple elements having a stable order in the future (i.e., they are resilient to refactoring).
Type Casting:
Bit types can be cast from one bit-width to another with the `as` keyword. Types can be widened (increasing bit-width), narrowed (decreasing bit-width) and/or changed between signed and unsigned. Some examples are found below.
```
#[test]
fn test_narrow_cast() {
  let twelve = u4:0b1100;
  assert_eq(twelve as u2, u2:0)
}

#[test]
fn test_widen_cast() {
  let three = u2:0b11;
  assert_eq(three as u4, u4:3)
}

#[test]
fn test_narrow_signed_cast() {
  let negative_seven = s4:0b1001;
  assert_eq(negative_seven as u2, u2:1)
}

#[test]
fn test_widen_signed_cast() {
  let negative_one = s2:0b11;
  assert_eq(negative_one as s4, s4:-1)
}

#[test]
fn test_widen_to_unsigned() {
  let negative_one = s2:0b11;
  assert_eq(negative_one as u3, u3:0b111)
}

#[test]
fn test_widen_to_signed() {
  let three = u2:0b11;
  assert_eq(three as u3, u3:0b011)
}
```
Type Checking and Inference:
DSLX performs type checking and produces an error if types in an expression don't match up.

`let` expressions also perform type inference, which is quite convenient. For example, instead of writing:
```
let ch: u32 = (e & f) ^ ((!e) & g);
let (h, g, f): (u32, u32, u32) = (g, f, e);
```
one can write the following, as long as the types can be properly inferred:
```
let ch = (e & f) ^ ((!e) & g);
let (h, g, f) = (g, f, e);
```
Note that type annotations can still be added and be used for program understanding, as they they will be checked by DSLX.

Type Inference Details:

Type Inference Background:
All expressions in the language's expression grammar have a deductive type inference rule. The types must be known for inputs to an operator/function and every expression has a way to determine its type from its operand expressions.

DSLX uses deductive type inference to check the types present in the program. Deductive type inference is a set of (typically straight-forward) deduction rules: Hindley-Milner style deductive type inference determines the result type of a function with a rule that only observes the input types to that function. (Note that operators like '+' are just slightly special functions in that they have pre-defined special-syntax-rule names.)
Bindings and Environment:
In DSLX code, the "environment" where names are bound (sometimes also referred to as a symbol table) is called the `Bindings` -- it maps identifiers to the AST node that defines the name (`{string: AstNode}`), which can be combined with a mapping from AST node to its deduced type (`{AstNode: ConcreteType}`) to resolve the type of an identifier in the program. `Let` is one of the key nodes that populates these `Bindings`, but anything that creates a bound name does as well (e.g. parameters, for loop induction variables, etc.).

Operator Example:
For example, consider the binary (meaning takes two operands) / infix (meaning it syntactically is placed in the center of its operands) '+' operator. The simple deductive type inference rule for '+' is:
```
(T, T) -> T
```
Meaning that the left hand side operand to the '+' operator is of some type (call it T), the right hand side operand to the '+' operator must be of that same type, T, and the result of that operator is then (deduced) to be of the same type as its operands, T.

Let's instantiate this rule in a function:
```
fn add_wrapper(x: bits[2], y: bits[2]) -> bits[2] {
  x + y
}
```
This function wraps the '+' operator. It presents two arguments to the '+' operator and then checks that the annotated return type on `add_wrapper` matches the deduced type for the body of that function; that is, we ask the following question of the '+' operator (since the type of the operands must be known at the point the add is performed):
```
(bits[2], bits[2]) -> ?
```
To resolve the '?' the following procedure is being used:

	1.Pattern match the rule given above `(T, T) -> T` to determine the type T: the left hand side operand is `bits[2]`, called T.
	2.Check that the right hand side is also that same T, which it is: another `bits[2]`.
	3.Deduce that the result type is that same type T: bits[2].
	4.That becomes the return type of the body of the function. Check that it is the same type as the annotated return type for the function, and it is!
The function is annotated to return `bits[2]`, and the deduced type of the body is also `bits[2]`. Qed.

Type errors:
A type error would occur in the following:
```
fn add_wrapper(x: bits[2], y: bits[3]) -> bits[2] {
  x + y
}
```
Applying the type deduction rule for '+' finds an inconsistency. The left hand side operand has type `bits[2]`, called T, but the right hand side is `bits[3]`, which is not the same as T. Because the deductive type inference rule does not say what to do when the operand types are different, it results in a type error which is flagged at this point in the program.

Let Bindings, Names, and the Environment:
In the DSL, `let` is an expression. It may not seem obvious at a glance, but it is! As a primer see the type inference background and how names are resolved in an environment.

"let" expressions are of the (Rust-inspired) form:
```
let $name: $annotated_type = $expr; $subexpr
```
`$name` gets "bound" to a value of type `$annotated_type`. The `let` typecheck rule must both check that `$expr` is of type `$annotated_type`, as well as determine the type of `$subexpr`, which is the type of the overall "let expression".

In this example, the result of the `let` expression is the return value -- `$subexpr` (`x+x`) can use the `$name` (`x`) which was "bound":
```
fn main(y: u32) -> u64 {
  let x: u64 = y as u64;
  x+x
}
```
If we invoke `main(u32:2)` we will the evaluate `let` expression -- it creates a binding of `x` to the value `u64:2`, and then evaluates the expression `x+x` in that environment, so the result of the `let` expression's `$subexpr` is `u64:4`.
