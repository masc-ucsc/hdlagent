module subtractor (
    input  [7:0] a,
    input  [7:0] b,
    output [7:0] diff
);
  assign diff = a - b;
endmodule

