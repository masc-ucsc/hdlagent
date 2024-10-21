module Prob018_mux256to1_spec(input [255:0] in, input [7:0] sel, output [0:0] out);
    assign out = in[sel];
endmodule
