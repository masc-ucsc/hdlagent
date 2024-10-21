module Prob027_fadd_spec(input [0:0] a, input [0:0] b, input [0:0] cin, output [0:0] cout, output [0:0] sum);
  assign sum = a ^ b ^ cin; // Sum is XOR of a, b, and cin
  assign cout = (a & b) | (a & cin) | (b & cin); // Carry out
endmodule
