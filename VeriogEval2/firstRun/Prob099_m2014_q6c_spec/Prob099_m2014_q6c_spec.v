module Prob099_m2014_q6c_spec(input [5:0] y, input [0:0] w, output [0:0] Y1, output [0:0] Y3);

    // Next-state logic for Y1 (y[1])
    assign Y1 = (y[0] & ~w) | (y[3] & w) | (y[4] & w);

    // Next-state logic for Y3 (y[3])
    assign Y3 = (y[1] & w) | (y[2] & w) | (y[5] & w);

endmodule
