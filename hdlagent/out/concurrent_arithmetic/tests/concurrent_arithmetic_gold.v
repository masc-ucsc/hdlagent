module concurrent_arithmetic (
    input  [3:0] a,
    input  [3:0] b,
    output [3:0] sum,
    output [3:0] diff
);
  assign sum  = a + b;
  assign diff = a - b;
endmodule


