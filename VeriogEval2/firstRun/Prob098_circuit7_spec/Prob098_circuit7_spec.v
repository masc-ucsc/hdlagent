module Prob098_circuit7_spec(input [0:0] clk, input [0:0] a, output reg [0:0] q);
  always @(posedge clk) begin
    if (a == 0)
      q <= 1;
    else
      q <= 0;
  end
endmodule
