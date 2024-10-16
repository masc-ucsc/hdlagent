module logical_or_spec(input [3:0] a, input [3:0] b, output [0:0] result);
  // Perform bitwise OR and reduce to a single OR result
  assign result = |(a | b);
endmodule
