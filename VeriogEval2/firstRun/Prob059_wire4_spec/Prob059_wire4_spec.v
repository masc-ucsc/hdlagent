module Prob059_wire4_spec(input [0:0] a, input [0:0] b, input [0:0] c, output [0:0] w, output [0:0] x, output [0:0] y, output [0:0] z);
    assign w = a; // Connect a to w
    assign x = b; // Connect b to x
    assign y = b; // Connect b to y
    assign z = c; // Connect c to z
endmodule
