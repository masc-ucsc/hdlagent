module left_shift(
  input [7:0] a,
  output [7:0] o
);

  assign o = {a[6:0], 2'b00};

endmodule