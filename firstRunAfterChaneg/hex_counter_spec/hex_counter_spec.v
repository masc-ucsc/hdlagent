module hex_counter_spec(input [0:0] clock, input [0:0] reset, output reg [3:0] q);

always @(*) begin
    if (reset)
        q = 4'b0000; // Synchronous reset
    else if (q == 4'b1111)
        q = 4'b0000; // Roll back to zero when q is F
    else
        q = q + 1; // Increment counter
end

endmodule
