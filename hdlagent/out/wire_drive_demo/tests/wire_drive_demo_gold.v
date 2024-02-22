module wire_drive_demo (
    input  a,
    input b,
    input sel,
    output w,
    output w1,
    output w2
);
  wire w1, w2;
  assign w1 = a & b;
  assign w2 = a | b;
  assign w  = sel ? w1 : w2;
endmodule


