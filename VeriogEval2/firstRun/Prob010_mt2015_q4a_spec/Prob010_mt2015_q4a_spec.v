module Prob010_mt2015_q4a_spec(input [0:0] x, input [0:0] y, output [0:0] z);
    assign z = (x ^ y) & x; // z = XOR of x and y, AND with x
endmodule
