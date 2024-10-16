module variable_logical_leftshift (
    input [4:0] shift_n_i,
    input [31:0] val_i,
    output [31:0] result_o
);
  assign result_o = val_i << shift_n_i;
endmodule

