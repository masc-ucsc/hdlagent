module Prob028_m2014_q4a_spec(input [0:0] d, input [0:0] ena, output reg [0:0] q);
    always @(*) begin
        if (ena) begin
            q = d;
        end
    end
endmodule
