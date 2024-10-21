module Prob020_mt2015_eq2_spec(input [1:0] A, input [1:0] B, output [0:0] z);

    // Compare the bits of A and B and assign 1 to z if equal, otherwise 0
	assign z = (A == B) ? 1'b1 : 1'b0;

endmodule
