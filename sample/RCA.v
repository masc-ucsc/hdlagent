
module RCA(input [7:0] a, input [7:0] b, input [7:0] c, output [10:0] foo);

    wire [8:0] sum_ab;
    wire [9:0] sum_abc;

    assign sum_ab = a + b;
    assign sum_abc = sum_ab + c;
    assign foo = sum_abc;
   
endmodule

