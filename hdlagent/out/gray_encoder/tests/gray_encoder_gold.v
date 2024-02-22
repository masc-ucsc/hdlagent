module gray_encoder (
    input  [3:0] binary_input,
    output [3:0] gray_code
);


  assign gray_code[3] = binary_input[3];


  assign gray_code[2] = binary_input[3] ^ binary_input[2];
  assign gray_code[1] = binary_input[2] ^ binary_input[1];
  assign gray_code[0] = binary_input[1] ^ binary_input[0];

endmodule






