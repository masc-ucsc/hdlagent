module PCG32(
    output reg [31:0] ouput_gen,
    input wire clk
);

reg [63:0] state;

localparam multiplier = 64'h5851f42d4c957f2d;
localparam increment = 64'h14057b7ef767814f;

initial begin
    state = 64'h123456789abcdef0;
end

always @(posedge clk) begin
    state <= (state * multiplier + increment) & 64'hFFFFFFFFFFFFFFFF;
    ouput_gen <= state[31:0] ^ (state[63:32] >> 18);
end

endmodule

