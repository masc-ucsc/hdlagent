module RippleCarryAdder (
    input  [3:0] a,
    input  [3:0] b,
    output [4:0] sum
);

  wire [3:0] co;
  FullAdder FA0 (
      .a  (a[0]),
      .b  (b[0]),
      .ci (1'b0),
      .sum(sum[0]),
      .co (co[0])
  );

  FullAdder FA1 (
      .a  (a[1]),
      .b  (b[1]),
      .ci (co[0]),
      .sum(sum[1]),
      .co (co[1])
  );

  FullAdder FA2 (
      .a  (a[2]),
      .b  (b[2]),
      .ci (co[1]),
      .sum(sum[2]),
      .co (co[2])
  );

  FullAdder FA3 (
      .a  (a[3]),
      .b  (b[3]),
      .ci (co[2]),
      .sum(sum[3]),
      .co (co[3])
  );
  assign sum[4] = co[3];
endmodule

module FullAdder (
    input  a,
    input  b,
    input  ci,
    output sum,
    output co
);

  assign {co, sum    } = a + b + ci;
endmodule

