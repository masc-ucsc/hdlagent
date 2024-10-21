module TopModule(input [0:0] clk, input [7:0] d, input [0:0] reset, output reg [7:0] q);

always @(negedge clk) begin
    if (reset) begin
        q <= 8'h34; // synchronous reset to 0x34
    end else begin
        q <= d;
    end
end

endmodule
