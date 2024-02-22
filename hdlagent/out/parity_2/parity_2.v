module parity_2(
  input  [3:0] abcd,
  output [0:0] P1,
  output [0:0] P2
);

// Combinational logic for even parity
assign P1 = ~(^abcd);

// Combinational logic for odd parity
assign P2 = ^abcd;

endmodule