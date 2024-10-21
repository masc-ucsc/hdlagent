module Prob085_shift4_spec(
    input  [0:0] clk,
    input  [0:0] areset,
    input  [0:0] load,
    input  [0:0] ena,
    input  [3:0] data,
    output reg [3:0] q
);

always @(posedge clk or posedge areset) begin
    if (areset) begin
        q <= 4'b0000; // Reset shift register to zero
    end else begin
        if (load) begin
            q <= data; // Load data into shift register
        end else if (ena) begin
            q <= {1'b0, q[3:1]}; // Right shift
        end
    end
end

endmodule
