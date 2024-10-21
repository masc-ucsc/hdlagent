module Prob069_truthtable1_spec(input [0:0] x3, input [0:0] x2, input [0:0] x1, output [0:0] f);

assign f = (~x3 & x2) | (x2 & x1);

endmodule
