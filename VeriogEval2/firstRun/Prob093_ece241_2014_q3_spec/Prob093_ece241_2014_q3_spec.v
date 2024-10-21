module Prob093_ece241_2014_q3_spec(input [0:0] c, input [0:0] d, output [3:0] mux_in);
    wire n_d;
    
    // Not gate for d
    assign n_d = ~d;

    // mux_in[0] = c'd + cd' = c ^ d
    assign mux_in[0] = c ^ d;
    
    // mux_in[1] = 0
    assign mux_in[1] = 1'b0;
    
    // mux_in[2] = c
    assign mux_in[2] = c;

    // mux_in[3] = 1
    assign mux_in[3] = 1'b1;
endmodule
