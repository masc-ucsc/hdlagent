module Prob013_m2014_q4e_spec(input [0:0] in1, input [0:0] in2, output [0:0] logic out);
    assign out = ~(in1 | in2); // 2-input NOR gate
endmodule
