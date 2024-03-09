**User:** I have been writing some DSLX code lately and I have come across a lot of syntax errors, let me show you what errors I have seen and how to avoid them.

ERROR example 1:
```
0007:   let a0 = a[0];
~~~~~~~~~~~~~~~~~~^-^ TypeInferenceError: uN[4] Value to index is not an array.
0008:   let a1 = a[1];
```

SOLUTION example 1:
DSLX does not use Verilog-style bit indexing, but rather Pythonic indexing. This means it is allowed to reverse index bits by using negative values, as well as specify ranges. In this case, if we want to index a single bit, we must specify a single bit range. Note: you can also concatenate the single bits into an array of bits through the "++" operator.
Fix:
```
let a0 = a[0:1];        // bit 0 as type bit[N]
let a1 = a[1:2] as u1;  // bit 1 cast as 1 bit log uInt

let a_concat = a0 ++ a1;
```

ERROR example 2:
```
0006:    let  a: u4 = u4:1;
0007:    let a0: u1 = a & u4:1;
~~~~~~~~~~~~~~~~~^^ XlsTypeError: uN[1] vs uN[4]: Annotated type did not match inferred type of right hand side expression.
```

SOLUTION example 2:
oSLX has a strict typechecking system which is engaged when a type is explicitly declared, such as "let a: u4" declares variable "a" to be a 4 bit long unsigned integer. Typecasting may be helpful when one needs to specify a type, despite the powerful implicit typesystem DSLX has to offer. It is done through the "as" keyword, which allows one to specify the desired type of the expression.
Fix:
```
0006:    let  a: u4 = u4:1;
0007:    let a0: u1 = (a & u4:1) as u1;  // convert to u1
```

ERROR example 3:
```
0006:   let out_signal = (sel == u2:0) ? in0 :
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^ ScanError: Unrecognized character: '?' (0x3f)
0007:                    (sel == u2:1) ? in1 :
0008:                    (sel == u2:2) ? in2 :
0009:                                    in3;
```

SOLUTION example 3:
DSLX does not have the Verilog/C style ternary operator, so the "?" character is not a keyword. Instead of attempting nested "if" statements, a case/switch may be emulated through DSLX pattern matching, done by its "match" keyword. This is similiar to Rust in that it matches a given pattern, and returns a value mapped to said pattern.
Fix:
```
let out_signal = match sel {
                   u2:0 => in0,
                   u2:1 => in1,
                   u2:2 => in2,
                   _ => in3
                 };
```

ERROR example 4:
```
0006:   let y = ~s & a;
~~~~~~~~~~~~~~~~^ ScanError: Unrecognized character: '~' (0x7e)
```

SOLUTION example 4:
DSLX does not use the "~" character to perform bitwise inversions, that is instead performed by the "!" character.
Fix:
```
0006:   let y = !s & a;
```

ERROR example 5:
```
0007:   let a = ^(b[0:8]);
~~~~~~~~~~~~~~~~^ ParseError: Expected start of an expression; got: ^
```

SOLUTION example 5:
Unlike Verilog, DSLX does not have unary reduction operators. The only unary operators are "!" for bitwise inversion, and "-" for two's complement negation. If one wished to peform a reduction operator, it must be done on every bit of the bit array. But since many operators do not work on bit[N] type, we must typecast as well for each bit isolated.
Fix:
```
0007:   let a = (b[0:1] as u1) ^ (b[1:2] as u1) ^ (b[2:3] as u1) ^ (b[3:4] as u1) ^ (b[4:5] as u1) ^ (b[5:6] as u1) ^ (b[6:7] as u1) ^ (b[7:8] as u1);
```

ERROR example 6:
```
0002:     let a: u3 = u3:1;
0003:     let b: u3 = u3:2;
0004:     let cin: u1 = u1:1;
0005:     let result = a + b + cin;
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^ XlsTypeError: uN[4] vs uN[1]: Could not deduce type for binary operation '+'
```

SOLUTION example 6:
All righthand side bitwidths and types must match when performing operations on variables. The lefthand side expects a 4 bit wide return value from adding a few 3 bit wide values, this expectation is not met due to the 1 bit wide value. In the case of a values type being inconvenient to change, a typecast may be called onto it when necessary.
Fix:
```
0002:     let a: u3 = u3:1;
0003:     let b: u3 = u3:2;
0004:     let cin: u1 = u1:1;
0005:     let result = a + b + (cin as u3);
```

ERROR example 7:
```
0010: struct ExampleStruct { out_o: u1, }
0011:
0012: fn ExampleFunct(in_i: u8) -> ExampleStruct {
0013:    let out_o = in_i & u8:1;
0015:    ExampleStruct { out_o: out_o }
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^------^ XlsTypeError: uN[1] vs uN[8]: Mismatch between member and argument types.
0016: }
```

SOLUTION example 7:
Bitwidths and types must also match on both sides of an assignment statement, including struct field assignments. It is best practice to name the value being assigned to the struct the same as a field, as well as to typecast the value being assigned to enforce type correctness.
Fix:
```
0010: struct ExampleStruct { out_o: u1, }
0011:
0012: fn ExampleFunct(in_i: u8) -> ExampleStruct {
0013:    let out_o = in_i & u8:1;
0015:    ExampleStruct { out_o: out_o as u1}
0016: }
```

ERROR example 8:
```
0008:   let mut accumulator: u8 = u8:0;
~~~~~~~~~~~~~~~~^---------^ ParseError: Expected '=', got 'identifier'
0009:   accumulator = accumulator + u8:1;
```

SOLUTION example 8:
DSLX is an immutable dataflow graph based hardware description language, therefore it does NOT have "mut" as a keyword or have otherwise mutable variables. All combinational logic statements must be immutable "let" assignments. Therefore it is best to create intermediate values and use those as a operands of the final assignment.
Fix:
```
0008:    let accumulator0: u8 = u8:0;   // use of intermediate values allows for incremental change to a final value
0009:    let accumulator: u8 = accumulator0 + u8:1;
```

ERROR example 9:
```
0006: fn example_funct(a: u8, b: u4) -> ExampleOutput {
0007:   assert(b != u4:0);
~~~~~~~~^----^ ParseError: Cannot find a definition for name: "assert"
0008:   let x = u8:1;
```

SOLUTION example 9:
Asserts are only supported for DSLX testbenches, meaning they should not exist within the logical implementation of a DSLX function. For this reason it is best to avoid their use in this context. Do not use assert statements and if they exist, delete them.
Fix:
```
0006: fn example_funct(a: u8, b: u4) -> ExampleOutput {
0007:   // deleted this line to avoid using assert statements
0008:   let x = u8:1;
```
