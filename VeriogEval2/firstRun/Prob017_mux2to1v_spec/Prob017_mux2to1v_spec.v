module Prob017_mux2to1v_spec(input [99:0] a, input [99:0] b, input [0:0] sel, output [99:0] out);
    assign out = sel ? b : a;
endmodule
