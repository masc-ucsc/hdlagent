**User:**
`trace_fmt!`:
DSLX supports printf-style debugging via the `trace_fmt!` builtin, which allows dumping of current values to stdout. For example:
```
// Note: to see `trace_fmt!` output you need to be seeing `INFO` level logging,
// enabled by adding the '--alsologtostderr' flag to the command line (among
// other means). For example:
// bazel run -c opt //xls/dslx:interpreter_main  /path/to/dslx/file.x -- --alsologtostderr

fn shifty(x: u8, y: u3) -> u8 {
  trace_fmt!("x: {:x} y: {}", x, y);
  // Note: y looks different as a negative number when the high bit is set.
  trace_fmt!("y as s8: {}", y as s2);
  x << y
}

#[test]
fn test_shifty() {
  assert_eq(shifty(u8:0x42, u3:4), u8:0x20);
  assert_eq(shifty(u8:0x42, u3:7), u8:0);
}
```
would produce the following output, with each trace being annotated with its corresponding source position:
```
[...]
[ RUN UNITTEST  ] test_shifty
I0510 14:31:17.516227 1247677 bytecode_interpreter.cc:994] x: 42 y: 4
I0510 14:31:17.516227 1247677 bytecode_interpreter.cc:994] y as s8: 4
I0510 14:31:17.516227 1247677 bytecode_interpreter.cc:994] x: 42 y: 7
I0510 14:31:17.516227 1247677 bytecode_interpreter.cc:994] y as s8: -1
[            OK ]
[...]
```
Note: `trace!` currently exists as a builtin but is in the process of being removed, as it provided the user with only a "global flag" way of specifying the desired format for output values -- `trace_fmt!` is more powerful.

`fail!`: assertion failure
The `fail!` builtin indicates dataflow that should not be occurring in practice. Its general signature is:
```
fail!(label, fallback_value)
```
The `fail!` builtin can be thought of as a "fatal assertion macro". It is used to annotate dataflow that should not occur in practice and, if triggered, should raise a fatal error in simulation (e.g. via a JIT-execution failure status or a Verilog assertion when running in RTL simulation).

Note, however, that XLS will permit users to avoid inserting fatal-error-signaling hardware that correspond to this `fail!` -- assuming it will not be triggered in practice minimizes its cost in synthesized form. In this situation, when it is "erased", it acts as the identity function, propagating the `fallback_value`. This allows XLS to keep well defined semantics even when fatal assertion hardware is not present.

Example: if only these two enum values shown should be possible (say, as a documented precondition for `main`):
```
enum EnumType: u2 {
  FIRST = 0,
  SECOND = 1,
}

fn main(x: EnumType) -> u32 {
  match x {
    EnumType::FIRST => u32:0,
    EnumType::SECOND => u32:1,
    _ => fail!("unknown_EnumType", u32:0),
  }
}
```
The `fail!("unknown_EnumType", u32:0)` above indicates that a) that match arm should not be reached (and if it is in the JIT or RTL simulation it will cause an error status or assertion failure respectively), but b) provides a fallback value to use (of the appropriate type) in case it were to happen in synthesized gates which did not insert fatal-error-indicating hardware.

The associated label (the first argument) must be a valid Verilog identifier and is used for identifying the failure when lowered to SystemVerilog. At higher levels in the stack, it's unused.

cover! :
NOTE: Currently, `cover!` has no effect in RTL simulators supported in XLS open source (i.e. iverilog).

The `cover!` builtin tracks how often some condition is satisfied. It desugars into SystemVerilog cover points. Its signature is:
```
cover!(<name>, <condition>);
```
Where `name` is a function-unique literal string identifying the coverpoint and `condition` is a boolean element. When `condition` is true, a counter with the given name is incremented that can be inspected upon program termination. Coverpoints can be used to give an indication of code "coverage", i.e. to see what paths of a design are exercised in practice. The name of the coverpoint must begin with either a letter or underscore, and its remainder must consist of letters, digits, underscores, or dollar signs.

gate!
The `gate!` builtin is used for operand gating, of the form:
```
let gated_value = gate!(<pass_value>, <value>);
```
This will generally use a special Verilog macro to avoid the underlying synthesis tool doing boolean optimization, and will turn `gated_value` to `0` when the predicate `pass_value` is `false`. This can be used in attempts to manually avoid toggles based on the gating predicate.

It is expected that XLS will grow facilities to inserting gating ops automatically, but manual user insertion is a practical step in this direction. Additionally, it is expected that if, in the resulting Verilog, gating occurs on a value that originates from a flip flop, the operand gating may be promoted to register-based load-enable gating.

Testing and Debugging:
DSLX allows specifying tests right in the implementation file via the `test` and `quickcheck` directives.

Having key test code in the implementation file serves two purposes. It helps to ensure the code behaves as expected. Additionally it serves as 'executable' documentation, similar in spirit to Python doc strings.

Unit Tests:
Unit tests are specified by the `test` directive, as seen below:
```
#[test]
fn test_reverse() {
  assert_eq(u1:1, rev(u1:1));
  assert_eq(u2:0b10, rev(u2:0b01));
  assert_eq(u2:0b00, rev(u2:0b00));
}
```
The DSLX interpreter will execute all functions that are proceeded by a `test` directive. These functions should be non-parametric, take no arguments, and should return a unit-type.

Unless otherwise specified in the implementation's build configs, functions called by unit tests are also converted to XLS IR and run through the toolchain's LLVM JIT. The resulting values from the DSLX interpreter and the LLVM JIT are compared against each other to assert equality. This is to ensure DSLX implementations are IR-convertible and that IR translation is correct.

QuickCheck:
QuickCheck is a testing framework concept founded on property-based testing. Instead of specifying expected and test values, `QuickCheck` asks for properties of the implementation that should hold true against any input of the specified type(s). In DSLX, we use the quickcheck directive to designate functions to be run via the toolchain's QuickCheck framework. Here is an example that complements the unit testing of DSLX's `rev` implementation from above:
```
// Reversing a value twice gets you the original value.

#[quickcheck]
fn prop_double_reverse(x: u32) -> bool {
  x == rev(rev(x))
}
```
The DSLX interpreter will also execute all functions that are proceeded by a `quickcheck` directive. These functions should be non-parametric and return a `bool`. The framework will provide randomized input based on the types of the arguments to the function (e.g. above, the framework will provided randomized `u32`'s as `x`).

By default, the framework will run the function against 1000 sets of randomized inputs. This default may be changed by specifying the `test_count` key in the `quickcheck` directive before a particular test:
```
#[quickcheck(test_count=50000)]
```
The framework also allows programmers to specify a seed to use in generating the random inputs, as opposed to letting the framework pick one. The seed chosen for production can be found in the execution log.

For determinism, the DSLX interpreter should be run with the `seed` flag: `./interpreter_main --seed=1234 <DSLX source file>```
