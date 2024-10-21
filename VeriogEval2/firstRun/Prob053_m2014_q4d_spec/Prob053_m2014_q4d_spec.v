module Prob053_m2014_q4d_spec(input [0:0] clk, input [0:0] in, output reg [0:0] out);
  wire xor_out;
  
  assign xor_out = in[0] ^ out[0]; // XOR operation
  
  always @(posedge clk[0]) begin
    out[0] <= xor_out; // D flip-flop captures xor_out on positive edge of clk
  end
  
endmodule
