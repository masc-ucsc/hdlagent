module sign_extend_int_to_double (
    input [31:0] int_i,
    output [63:0] double_o
);
  wire [31:0] s_ext_w;
  assign s_ext_w = int_i[31] == 1'b1 ? 32'hFFFFFFFF : 32'd0;
  assign double_o = {s_ext_w, int_i};
endmodule


