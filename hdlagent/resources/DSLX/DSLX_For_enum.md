**User:** `for` expressions:
In the following document we explain in detail the implementation of routine to compute a CRC32 checksum on a single 8-bit input. We don't discuss the algorithm here, only the language features necessary to implement the algorithm.

Function Prototype:
The signature and first line of this function should look familiar enough now, but the `for` construct is new: DSLX provides a means of iterating a fixed number of times within a function.

A DSLX `for` loop has the following structure:

1.The loop signature: this consists of three elements: 1. An (index, ) tuple. The index holds the current iteration number, and the accumulator vars are user-specified data carried into the current iteration. 2. The type specification for the index/accumulators tuple. Note that the index type can be controlled by the user (i.e., doesn't have to be u32, but it should be able to hold all possible loop index values). 3. An iterable, either the `range()` or `enumerate()` expressions, either of which dictates the number of iterations of the loop to complete.
2.The loop body: this has the same general form as a DSLX function. Particularly noteworthy is that the loop body ends by stating the "return" value. In a `for` loop, this "return" value is either used as the input to the next iteration of the loop (for non-terminal iterations) or as the result of the entire expression (for the terminal iteration).

For this specific for loop, the index variable and accumulator are `i` and `crc`, both of type `u32`. The iterable range expression specifies that the loop should execute 8 times.
```
// 8 rounds of updates.
  for (i, crc): (u32, u32) in range(u32:8) {
```
At the end of the loop, the calculated value is being assigned to the accumulator `crc` - the last expression in the loop body is assigned to the accumulator:
```
    let mask: u32 = -(crc & u32:1);
    (crc >> u32:1) ^ (polynomial & mask)
```
Finally, the accumulator's initial value is being passed to the `for` expression as a parameter. This can be confusing, especially when compared to other languages, where the init value typically is provided at or near the top of a loop.
```
}(crc)
```
Since the `for` loop is the last expression in the function, it's also the function's return value, but in other contexts, it could be assigned to a variable and used elsewhere. In general, the result of a `for` expression can be used in the same manner as any other expression's result.

`enumerate` and `match` expressions:
In the following document we explain in detail the implementation of a 8 byte prefix scan computation. In order to understand the implementation, it is useful to understand the intended functionality first.

For a given input of 8 bytes, the scan iterates from left to right over the input and produces an output of the same size. Each element in the output contains the count of duplicate values seen so far in the input. The counter resets to 0 if a new value is found.

For example, for this input:
```
let input = u32[8]:[0, ...]
```
the code should produce this output:
```
  u3[8]:[0, 1, 2, 3, 4, 5, 6, 7])
```
At index 0 it has not yet found any value, so it assigns a counter value of `0`.

At index 1 it finds the second occurrence of the value '0' (which is the 1st duplicate) and therefore adds a 1 to the counter from index 0.

At index 2 it finds the third occurrence of the value '0' (which is the 2nd duplicate) and therefore adds a 1 to the counter from index 1. And so on.

Correspondingly, for this input:
```
  let input = u32[8]:[0, 0, 1, 1, 2, 2, 3, 3]
```
it should produce:
```
assert_eq(result, u3[8]:[0, 1, 0, 1, 0, 1, 0, 1])
```
The full listing is in `examples/dslx_intro/prefix_scan_equality.x`.

Function `prefix_scan_eq`:
The implementation displays a few interesting language features.

The function prototype is straight-forward. Input is an array of 8 values of type `u32`. Output is an array of size 8 holding 3-bit values (the maximum resulting count can only be 7, which fits in 3 bits).
```
fn prefix_scan_eq(x: u32[8]) -> u3[8] {
```
The first let expression produces a tuple of 3 values. It only cares about the last value result, so it stubs out the other two elements via the 'ignore' placeholder _.
```
  let (_, _, result) =
```
Why a 3-Tuple? Because he following loop has tuple of three values as the accumulator. The return type of the loop is the type of the accumulator, so above let needs to be of the same type.

Enumerated Loop:
Using tuples as the accumulator is a convenient way to model multiple loop-carried values:
```
    for ((i, elem), (prior, count, result)): ((u32, u32), (u32, u3, u3[8]))
          in enumerate(x) {
```
The iterable of this loop is `enumerate(x)`. On each iteration, this construct delivers a tuple consisting of current index and current element. This is represented as the tuple `(i, elem)` in the `for` construct.

The loop next specifies the accumulator, which is a 3-tuple consisting of the values named `prior`, `count`, and `result`.
The types of the iterable and accumulator are specified next. The iterable is a tuple consisting of two `u32` values. The accumulator is more interesting, it is a tuple consisting of a `u32` value (`prior`), a `u3` value (`count`), and an array type `u3[8]`, which is an array holding 8 elements of bit-width 3. This is the type of `result` in the accumulator.

Looping back to the prior `let` statement, it ignores the `prior` and `count` members of the tuple and will only return the `result` part.

A Match Expression:
The next expression is an interesting `match` expression. The let expression binds the tuple `(to_place, new_count): (u3, u3)` to the result of the following match expression:
```
let (to_place, new_count): (u3, u3) = match (i == u32:0, prior == elem) {
```
`to_place` will hold the value that is to be written at a given index. `new_count` will contain the updated counter value.

The `match` expression evaluates two conditions in parallel:

	is `i` == 0?
	is the `prior` element the same as the current `elem`
Two tests mean there are four possible cases, which are all handled in the following four cases:
```
// i == 0 (no matter whether prior == elem or not):
      //    we set position 0 to 0 and update the new_counter to 1
      (true, true) => (u3:0, u3:1),
      (true, false) => (u3:0, u3:1),

      // if i != 0 - if the current element is the same as pior,
      //    set to_place to the value of the current count
      //    update new_counter with the increased counter value
      (false, true) => (count, count + u3:1),

      // if i != 0 - if current element is different from prior,
      //     set to_place back to 0
      //     set new_counter back to 1
      (false, false) => (u3:0, u3:1),
    };
```
To update the result, we set index `i` in the `result` array to the value `to_place` via the built-in `update` function, which produces a new value `new_result`:
```
let new_result: u3[8] = update(result, i, to_place);
```
Finally the updated accumulator value is constructed, it is the last expression in the loop:
```
    (elem, new_count, new_result)
```
Following the loop body, as an argument to the loop, we initialize the accumulator in the following way.

set element `prior` to -1, in order to not match any other value.
set element `count` to 0.
set element `result` to 8 0's of size `u3`. (Note that the `...` syntax is short for "fill in the rest of the elements with the last value specified".)
```
}((u32:-1, u3:0, u3[8]:[0, ...]));
```
And, finally, the function simply returns `result`:
```
  result
}
```
Testing:
To test the two cases we've described above, we add the following two test cases right to this implementation file:
```
#[test]
fn test_prefix_scan_eq_all_zero() {
  let input = u32[8]:[0, ...];
  let result = prefix_scan_eq(input);
  assert_eq(result, u3[8]:[0, 1, 2, 3, 4, 5, 6, 7])
}

#[test]
fn test_prefix_scan_eq_doubles() {
  let input = u32[8]:[0, 0, 1, 1, 2, 2, 3, 3];
  let result = prefix_scan_eq(input);
  assert_eq(result, u3[8]:[0, 1, 0, 1, 0, 1, 0, 1])
}
```
To run tests against the file present in the repository:
```
xls$ bazel run -c opt //xls/dslx:interpreter_main -- \
       $PWD/xls/examples/dslx_intro/prefix_scan_equality.x \
       --compare=none
[ RUN UNITTEST  ] prefix_scan_eq_all_zero_test
[            OK ]
[ RUN UNITTEST  ] prefix_scan_eq_doubles_test
[            OK ]
[===============] 2 test(s) ran; 0 failed; 0 skipped.
```
(Note that `--compare=none` is currently required because `enumerate` ranges are not currently convertable to IR, otherwise running the DSLX interpreter would do implicit comparison to IR interpreter )
