module A(input [0:0] x, input [0:0] y, output [0:0] z);
    assign z = (x ^ y) & x;
endmodule
module B(input [0:0] x, input [0:0] y, output [0:0] z);
    assign z = (~x & ~y) | (x & y);
endmodule
module Prob131_mt2015_q4_spec(input [0:0] x, input [0:0] y, output [0:0] z);
    wire [0:0] a1_out, a2_out, b1_out, b2_out;
    wire [0:0] or_out, and_out;

    A a1 (.x(x), .y(y), .z(a1_out));
    B b1 (.x(x), .y(y), .z(b1_out));
    A a2 (.x(x), .y(y), .z(a2_out));
    B b2 (.x(x), .y(y), .z(b2_out));

    assign or_out = a1_out | b1_out;
    assign and_out = a2_out & b2_out;
    assign z = or_out ^ and_out;
endmodule
