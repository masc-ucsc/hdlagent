module Prob070_ece241_2013_q2_spec(
    input [0:0] a,
    input [0:0] b,
    input [0:0] c,
    input [0:0] d,
    output [0:0] out_sop,
    output [0:0] out_pos
);

    // Sum-of-products (SOP) form
    assign out_sop = (~a & b & c & ~d) | // Represents input 2: 0,1,0,0
                     (a & b & c & d) |   // Represents input 15: 1,1,1,1
                     (~a & b & c & d);   // Represents input 7: 0,1,1,1

    // Product-of-sums (POS) form
    assign out_pos = (a | ~b | ~c | d) & // Represents ~input 0, 1, 4, 5, 6, 9, 10, 13, 14
                     (a | ~b | ~c | ~d) &
                     (a | b | c | ~d) &
                     (~a | ~b | ~c | ~d);

endmodule
