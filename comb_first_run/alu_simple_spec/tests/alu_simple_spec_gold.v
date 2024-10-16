module mux (
    input [1:0] sel,
    input [7:0] i0,
    input [7:0] i1,
    input [7:0] i2,
    output reg [7:0] out_o
);
  always @(sel, i0, i1, i2) begin
    case (sel)
      2'b00:   out_o = i0;
      2'b01:   out_o = i1;
      2'b10:   out_o = i2;
      default: out_o = 8'b00000000;
    endcase
  end
endmodule

