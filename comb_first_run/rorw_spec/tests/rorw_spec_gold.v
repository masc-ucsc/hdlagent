module basic_logic (
    input  [3:0] A,
    input  [3:0] B,
    output [3:0] O1,
    output [3:0] O2
);
  assign O1 = A & B;
  assign O2 = A | B;
endmodule

