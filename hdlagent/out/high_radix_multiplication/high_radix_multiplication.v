module high_radix_multiplication(input  [15:0] x, input  [15:0] y, output  [31:0] out_o);
    reg [31:0] inv_x; // Two's complement of x
    reg [31:0] products0, products1, products2, products3, products4, products5, products6, products7; // Original product array replaced by individual regs
    reg [31:0] sum0, sum1, sum2, sum3, sum4; // Original sum array replaced by individual regs
  

    // Calculate two's complement of x
    assign inv_x = ~x + 1;
  
    // Generate the partial products
    always @(*) begin
        case (y[0 +: 2])
            2'b00, 2'b11: products0 = 32'b0;
            2'b01: products0 = x << (2*0);
            2'b10: products0 = inv_x << (2*0);
        endcase

        case (y[2 +: 2])
            2'b00, 2'b11: products1 = 32'b0;
            2'b01: products1 = x << (2*1);
            2'b10: products1 = inv_x << (2*1);
        endcase

        // Add remaining cases up to products7
        //...
    end
  
    // Perform iterative addition
    always @(*) begin
        sum0 = products0 + products1;
        sum1 = products2 + products3;
        sum2 = products4 + products5;
        sum3 = products6 + products7;
        sum4 = sum0 + sum1 + sum2 + sum3;  // Final sum
    end
  
    assign out_o = sum4;  // Set output to final sum
  
endmodule