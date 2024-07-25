
module RCA(
    input [7:0] a,   // First 8-bit input operand
    input [7:0] b,   // Second 8-bit input operand
    input [7:0] c,   // Third 8-bit input operand
    output [10:0] foo // 11-bit output to store the result of (a + b + c)
);
    wire [8:0] sum_ab; // Intermediate sum of a and b (9 bits to account for carry)
    wire [9:0] sum_abc; // Intermediate sum of sum_ab and c (10 bits to account for carry)
    
    // Ripple Carry Adder for a + b
    assign sum_ab = a + b;

    // Ripple Carry Adder for sum_ab + c
    assign sum_abc = sum_ab + c;

    // Assign the final sum to foo
    assign foo = sum_abc;

endmodule

