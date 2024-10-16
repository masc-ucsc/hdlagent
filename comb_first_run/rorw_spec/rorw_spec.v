module rorw_spec(input [31:0] rs1, input [31:0] rs2, output [31:0] rd);
  wire [4:0] shift_amount = rs2[4:0];           // Extract least-significant 5 bits of rs2
  wire [31:0] rotated_word = {rs1[15:0], rs1[31:16]} >> shift_amount | {rs1[15:0], rs1[31:16]} << (32-shift_amount);
  assign rd = {32{rotated_word[31]}} | rotated_word;  // Sign-extend and assign to rd
endmodule
