module ripple_carry_adder_8bit(input [7:0] a, input [7:0] b, input [0:0] cin, output[7:0] sum, output[0:0] cout);
    wire [8:0] c;

    assign sum[0] = a[0] ^ b[0] ^ cin;
    assign c[1] = (a[0] & b[0]) | (a[0] & cin) | (b[0] & cin);
 
    assign sum[1] = a[1] ^ b[1] ^ c[1];
    assign c[2] = (a[1] & b[1]) | (a[1] & c[1]) | (b[1] & c[1]);

    // Repeat for sum[2] to sum[6] and c[2] to c[6] using c[3] to c[7]
 
    assign sum[7] = a[7] ^ b[7] ^ c[7];
    assign cout = (a[7] & b[7]) | (a[7] & c[7]) | (b[7] & c[7]);
endmodule