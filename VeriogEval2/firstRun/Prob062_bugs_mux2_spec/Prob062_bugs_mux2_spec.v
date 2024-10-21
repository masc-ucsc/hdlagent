module Prob062_bugs_mux2_spec(input [0:0] sel, input [7:0] a, input [7:0] b, output [7:0] out);
    assign out = (sel ? b : a);
endmodule
