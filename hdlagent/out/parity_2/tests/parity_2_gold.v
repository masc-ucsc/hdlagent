module parity_2 (
    input [3:0] abcd,
    output P1,
    output P2
);
  assign P1 = abcd[3] ^ abcd[2] ^ abcd[1] ^ abcd[0];
  assign P2 = ~(abcd[3] ^ abcd[2] ^ abcd[1] ^ abcd[0]);

endmodule






