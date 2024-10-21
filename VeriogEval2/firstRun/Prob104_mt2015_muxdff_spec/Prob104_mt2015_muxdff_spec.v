module Prob104_mt2015_muxdff_spec(input [0:0] clk, input [0:0] L, input [0:0] q_in, input [0:0] r_in, output [0:0] Q);

  wire [2:0] q;
  wire [2:0] d;

  TopModule u0 (.clk(clk), .L(L), .q_in(q[0]), .r_in(r_in), .Q(d[0]));
  TopModule u1 (.clk(clk), .L(L), .q_in(q[1]), .r_in(r_in), .Q(d[1]));
  TopModule u2 (.clk(clk), .L(L), .q_in(q[2]), .r_in(r_in), .Q(d[2]));

  assign Q = q[0];

  full_module full_inst (.r(d), .L(L), .clk(clk), .q(q));

endmodule
module TopModule(input clk, input L, input q_in, input r_in, output Q);
  wire mux_out;
  
  assign mux_out = L ? r_in : q_in;
  assign Q = mux_out;

endmodule
module full_module(input [2:0] r, input L, input clk, output reg [2:0] q);
  always @(posedge clk) begin
    if (L) begin
      q <= r;
    end else begin
      q <= {q[1] ^ q[2], q[0], q[2]};
    end
  end
endmodule
