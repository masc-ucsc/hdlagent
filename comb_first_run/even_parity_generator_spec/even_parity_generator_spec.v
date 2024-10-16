module even_parity_generator_spec(input [7:0] in_i, output [0:0] parity_out);
    assign parity_out = ~(in_i[0] ^ in_i[1] ^ in_i[2] ^ in_i[3] ^ in_i[4] ^ in_i[5] ^ in_i[6] ^ in_i[7]);
endmodule
