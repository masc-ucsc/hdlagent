module xnor_reduction (
    input [7:0] reduce_i,
    output result_o
);
  assign result_o = ~^reduce_i;
endmodule

