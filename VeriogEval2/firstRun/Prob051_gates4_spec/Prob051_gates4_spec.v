module TopModule(
    input [3:0] in,
    output [0:0] out_and,
    output [0:0] out_or,
    output [0:0] out_xor
);

    // Implement 4-input AND gate
    assign out_and = in[3] & in[2] & in[1] & in[0];
    
    // Implement 4-input OR gate
    assign out_or = in[3] | in[2] | in[1] | in[0];
    
    // Implement 4-input XOR gate
    assign out_xor = in[3] ^ in[2] ^ in[1] ^ in[0];

endmodule
