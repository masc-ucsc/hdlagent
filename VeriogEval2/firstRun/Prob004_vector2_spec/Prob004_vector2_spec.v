module Prob004_vector2_spec(input [31:0] in, output [31:0] out);
  assign out[31:24] = in[7:0];    // Reverse the first byte to be the last
  assign out[23:16] = in[15:8];   // Reverse the second byte to be the third
  assign out[15:8]  = in[23:16];  // Reverse the third byte to be the second
  assign out[7:0]   = in[31:24];  // Reverse the last byte to be the first
endmodule
