module clmul_spec(input [31:0] rs1, input [31:0] rs2, output [31:0] rd);
    wire [63:0] product_steps[31:0];
    assign product_steps[0] = rs2[0] ? {32'b0, rs1} : 64'b0;
    
    genvar i;
    generate
        for (i = 1; i < 32; i = i + 1) begin : clmul_loop
            assign product_steps[i] = rs2[i] ? (product_steps[i-1] ^ ({32'b0, rs1} << i)) : product_steps[i-1];
        end
    endgenerate

    assign rd = product_steps[31][31:0];
endmodule
