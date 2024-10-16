module bin_to_gray_spec(input [3:0] bin_in, output [3:0] gray_out);
    // Calculate Gray code from binary input
    assign gray_out[3] = bin_in[3]; // MSB remains the same
    assign gray_out[2] = bin_in[3] ^ bin_in[2];
    assign gray_out[1] = bin_in[2] ^ bin_in[1];
    assign gray_out[0] = bin_in[1] ^ bin_in[0];
endmodule
