module Prob033_ece241_2014_q1c_spec(input [7:0] a, input [7:0] b, output [7:0] s, output [0:0] overflow);
    assign s = a + b;
    assign overflow = (a[7] & b[7] & ~s[7]) | (~a[7] & ~b[7] & s[7]);
endmodule
