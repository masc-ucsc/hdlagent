module Prob078_dualedge_spec(input [0:0] clk, input [0:0] d, output [0:0] q);
  wire q1, q2;

  // Positive edge triggered D flip-flop
  reg q1_reg;
  always @(posedge clk) begin
    q1_reg <= d;
  end
  assign q1 = q1_reg;

  // Negative edge triggered D flip-flop
  reg q2_reg;
  always @(negedge clk) begin
    q2_reg <= d;
  end
  assign q2 = q2_reg;

  // Combinational logic OR gate to mimic dual-edge behavior
  assign q = q1 | q2;
endmodule
