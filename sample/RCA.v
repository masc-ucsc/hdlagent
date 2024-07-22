
module RCA(input [7:0] a, input [7:0] b, input [7:0] c, output [10:0] foo);

    wire [7:0] sum_ab;
    wire carry_ab;
    
    assign {carry_ab, sum_ab} = a + b; // Sum of a and b with carry out

    assign foo = sum_ab + c + carry_ab; // Sum of sum_ab, c, and carry_ab

endmodule

