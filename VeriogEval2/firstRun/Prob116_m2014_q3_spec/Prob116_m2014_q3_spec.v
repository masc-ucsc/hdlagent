module TopModule(input [3:0] x, output f);
    
    // Intermediate wires for easier reading
    wire x1, x2, x3, x4;
    
    assign {x1, x2, x3, x4} = x;
    
    // Assign output f based on the K-map interpretation
    assign f = (x3 & ~x2) | (~x3 & x1) | (x4 & x1 & ~x2);

endmodule
