module Prob123_bugs_addsubz_spec(input [0:0] do_sub, input [7:0] a, input [7:0] b, output [7:0] out, output [0:0] result_is_zero);
  wire [7:0] b_complement;
  wire [7:0] sum;

  // Complement b if performing subtraction
  assign b_complement = do_sub ? ~b : b;

  // Perform the addition/subtraction operation
  assign sum = a + b_complement + do_sub;

  // Assign the result to out
  assign out = sum;

  // Check if the result is zero
  assign result_is_zero = (sum == 8'b00000000);

endmodule
