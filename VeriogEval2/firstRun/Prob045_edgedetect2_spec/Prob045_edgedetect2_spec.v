module Prob045_edgedetect2_spec(input [0:0] clk, input [7:0] in, output reg [7:0] anyedge);
  reg [7:0] prev_in;

  always @(posedge clk) begin
    anyedge <= (prev_in ^ in) & in;
    prev_in <= in;
  end
endmodule
