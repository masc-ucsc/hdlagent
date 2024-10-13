module zero_extend_int_to_double (
    input [31:0] int_i,
    output [63:0] double_o
);
  assign double_o = {32'd0, int_i};
endmodule

