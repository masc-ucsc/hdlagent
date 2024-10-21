module Prob025_reduction_spec(
    input [7:0] in,
    output [0:0] parity
);

assign parity = ^in; // XOR all the bits in 'in' for even parity

endmodule
