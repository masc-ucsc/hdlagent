module multiplier_spec(input [3:0] a, input [3:0] b, output [7:0] product);
    assign product = a * b; // Multiplying 4-bit numbers to get 8-bit product
endmodule
