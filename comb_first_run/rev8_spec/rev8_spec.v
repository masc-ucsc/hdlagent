module rev8_spec(input [31:0] rs, output [31:0] rd);

    assign rd[31:24] = rs[7:0];   // Reverse the order of bytes
    assign rd[23:16] = rs[15:8];
    assign rd[15:8]  = rs[23:16];
    assign rd[7:0]   = rs[31:24];

endmodule
