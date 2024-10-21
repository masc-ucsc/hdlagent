module Prob011_norgate_spec(input [0:0] a, input [0:0] b, output [0:0] out);
    assign out = ~(a | b); // NOR gate logic
endmodule
