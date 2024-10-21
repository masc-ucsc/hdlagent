module Prob091_2012_q2b_spec(input [5:0] y, input [0:0] w, output [0:0] Y1, output [0:0] Y3);
    // Y1 is the condition for transitioning to state B
    assign Y1 = y[0] & w;

    // Y3 is the condition for transitioning to state D
    assign Y3 = (y[1] & ~w) | (y[2] & ~w) | (y[5] & ~w);
endmodule
