
module RCA(input [7:0] a, input [7:0] b, input [7:0] c, output [10:0] foo);

    // Internal wires for full bit addition including carries
    wire [8:0] sum_ab;
    wire [9:0] sum_abc;

    // First stage addition a + b
    assign sum_ab = a + b;

    // Second stage addition (a + b) + c
    assign sum_abc = sum_ab + c;

    // Assign the full sum to the output foo
    assign foo = sum_abc;

endmodule

