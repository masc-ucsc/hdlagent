module even_parity_generator (
    input [7:0] in_i,
    output parity_out
);
  assign parity_out = ^(in_i[7:0]);
endmodule

