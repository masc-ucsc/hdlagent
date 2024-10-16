module simple_concatenation (
    input [7:0] a_i,
    input [7:0] b_i,
    output [15:0] result_o
);
  assign result_o = {a_i, b_i};
endmodule

