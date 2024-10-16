module concurrent_arithmetic_spec(input [3:0] a, input [3:0] b, output [3:0] sum, output [3:0] diff);
    assign sum = a + b;   // Concurrent addition
    assign diff = a - b;  // Concurrent subtraction
endmodule
