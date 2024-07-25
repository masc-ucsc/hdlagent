
module RCA(input [7:0] a, input [7:0] b, input [7:0] c, output [10:0] foo);
  wire [8:0] sum_ab;    // 9-bit sum of a and b
  wire [8:0] sum_abc;   // 9-bit sum of sum_ab and c
  wire [10:0] final_sum; // 11-bit final sum

  assign sum_ab = a + b;
  assign sum_abc = sum_ab + c;
  assign final_sum = {2'b00, sum_abc[8:0]} + sum_ab[8];
  assign foo = final_sum;

endmodule

