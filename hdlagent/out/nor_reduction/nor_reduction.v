module nor_reduction(
  input [7:0] reduce_i,
  output [0:0] result_o
);
  assign result_o = ~(|reduce_i);
endmodule