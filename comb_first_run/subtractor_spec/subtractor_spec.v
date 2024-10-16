module subtractor_spec(input [7:0] a, input [7:0] b, output [7:0] diff);

    // Calculate diff using bitwise operations to subtract b from a
    assign diff = a - b; 

endmodule
