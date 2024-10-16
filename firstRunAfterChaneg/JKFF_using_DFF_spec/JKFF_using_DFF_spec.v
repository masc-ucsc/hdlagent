module JKFF_using_DFF_spec(input [0:0] clk, input [0:0] rst, input [0:0] j, input [0:0] k, output [0:0] q);
  wire d; // Internal wire to connect DFF input

  // Combinational logic to derive D input for DFF
  assign d = (j & ~q) | (~k & q);

  // Instantiate DFF submodule
  DFF dff_inst(.clk(clk), .rst(rst), .d(d), .q(q));

endmodule
module DFF(input [0:0] clk, input [0:0] rst, input [0:0] d, output reg [0:0] q);
  always @(posedge clk or posedge rst) begin
    if (rst)
      q <= 1'b0; // Reset the output
    else
      q <= d; // Capture D input on rising edge
  end
endmodule
