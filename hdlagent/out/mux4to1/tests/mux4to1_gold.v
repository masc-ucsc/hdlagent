module mux4to1 (
output    out_o,
input    in0,
input    in1,
input    in2,
input    in3,
input [1:0]    sel
);

  always_comb begin
    case (sel)
      2'b00:   out_o = in0;
      2'b01:   out_o = in1;
      2'b10:   out_o = in2;
      2'b11:   out_o = in3;
      default: out_o = 0;
    endcase
  end
endmodule



