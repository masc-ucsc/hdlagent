
module RCA(input [7:0] a, input [7:0] b, input [7:0] c, output [10:0] foo);
    wire [8:0] sum_ab;  // Intermediate sum for a + b
    wire [9:0] sum_abc; // Intermediate sum for (a + b) + c

    assign sum_ab = a + b;         // Sum of a and b
    assign sum_abc = sum_ab + c;   // Sum of (a + b) and c
    assign foo = sum_abc;          // Assign the final result to foo
endmodule

