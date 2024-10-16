module zero_extend_int_to_double_spec(input [31:0] int_i, output [63:0] double_o);
    assign double_o = {32'b0, int_i}; // Zero-extend the int_i to 64 bits
endmodule
