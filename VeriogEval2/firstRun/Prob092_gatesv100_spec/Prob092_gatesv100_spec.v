module TopModule(
    input [99:0] in,
    output [99:0] out_both,
    output [99:0] out_any,
    output [99:0] out_different
);
    
    // Compute out_both
    assign out_both[99] = 0;
    genvar i_both;
    generate
        for (i_both = 0; i_both < 99; i_both = i_both + 1) begin
            assign out_both[i_both] = in[i_both] & in[i_both + 1];
        end
    endgenerate
    
    // Compute out_any
    assign out_any[0] = 0;
    genvar i_any;
    generate
        for (i_any = 1; i_any < 100; i_any = i_any + 1) begin
            assign out_any[i_any] = in[i_any] | in[i_any - 1];
        end
    endgenerate
    
    // Compute out_different
    genvar i_different;
    generate
        for (i_different = 0; i_different < 99; i_different = i_different + 1) begin
            assign out_different[i_different] = in[i_different] ^ in[i_different + 1];
        end
        assign out_different[99] = in[99] ^ in[0]; // Wrap-around case
    endgenerate

endmodule
