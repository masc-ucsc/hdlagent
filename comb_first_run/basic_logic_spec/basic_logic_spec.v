module basic_logic_spec(input [3:0] A, input [3:0] B, output [3:0] O1, output [3:0] O2);
  assign O1 = A & B; // O1 is the result of A AND B
  assign O2 = A | B; // O2 is the result of A OR B
endmodule
