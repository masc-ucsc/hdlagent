module Prob031_dff_spec(input [0:0] clk, input [0:0] d, output reg [0:0] q);
    always @(posedge clk) begin
        q <= d;
    end
endmodule
