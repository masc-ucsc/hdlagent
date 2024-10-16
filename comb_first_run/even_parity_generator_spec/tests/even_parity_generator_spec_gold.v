module logical_or (
    input  [3:0] a,
    input  [3:0] b,
    output [0:0] result
);
  assign result = a || b;
endmodule

