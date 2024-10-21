module TopModule(input a, input b, input c, input d, output out);
  assign out = (~a & ~b & ~c & 1'b1) |   // 00 00
               (~a & ~b &  c & 1'b1) |   // 00 01
               (~a & ~b & ~d & 1'b1) |   // 00 10
               (~a &  b & ~c & 1'b1) |   // 01 00
               (~a &  b &  d & 1'b1) |   // 01 10
               ( a &  b &  c & 1'b1) |   // 11 01
               ( a &  b & ~d & 1'b1) |   // 11 10
               ( a & ~b &  c & 1'b1) ;   // 10 01
endmodule
