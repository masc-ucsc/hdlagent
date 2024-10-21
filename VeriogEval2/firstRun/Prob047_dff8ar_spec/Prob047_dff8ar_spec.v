module Prob047_dff8ar_spec(input [0:0] clk, input [7:0] d, input [0:0] areset, output [7:0] q);
    reg [7:0] q_reg;

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            q_reg <= 8'b0;
        end else begin
            q_reg <= d;
        end
    end

    assign q = q_reg;
endmodule
