module TopModule(input [0:0] a, input [0:0] b, output [0:0] sum, output [0:0] cout);
    assign sum = a ^ b;  // XOR for sum
    assign cout = a & b; // AND for carry out
endmodule
