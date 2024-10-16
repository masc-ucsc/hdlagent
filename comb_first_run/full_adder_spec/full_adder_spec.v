module full_adder_spec(input [0:0] a, input [0:0] b, input [0:0] cin, output [0:0] sum, output [0:0] cout);
  assign sum = a ^ b ^ cin;  // sum is calculated using XOR
  assign cout = (a & b) | (b & cin) | (cin & a);  // carry-out is calculated using OR of ANDs
endmodule
