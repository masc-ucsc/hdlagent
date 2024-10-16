module gray_encoder_spec(input [3:0] binary_input, output [3:0] gray_code);

  // MSB gray_code is the same as MSB binary_input
  assign gray_code[3] = binary_input[3];

  // Following bits are computed using XOR of consecutive bits
  assign gray_code[2] = binary_input[3] ^ binary_input[2];
  assign gray_code[1] = binary_input[2] ^ binary_input[1];
  assign gray_code[0] = binary_input[1] ^ binary_input[0];

endmodule
