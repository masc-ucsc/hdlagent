module Prob042_vector4_spec(input [7:0] in, output [31:0] out);
  assign out = { {24{in[7]}}, in }; // Sign-extend by replicating the sign bit 24 times
endmodule
