module Prob115_shift18_spec(
    input [0:0] clk,
    input [0:0] load,
    input [0:0] ena,
    input [1:0] amount,
    input [63:0] data,
    output reg [63:0] q
);
    always @(posedge clk) begin
        if (load) begin
            q <= data; // Load data to q
        end else if (ena) begin
            case (amount)
                2'b00: q <= q << 1;            // Shift left by 1
                2'b01: q <= q << 8;            // Shift left by 8
                2'b10: q <= {q[63], q[63:1]};  // Arithmetic shift right by 1
                2'b11: q <= { {8{q[63]}}, q[63:8] }; // Arithmetic shift right by 8
                default: q <= q;               // Default case, hold value
            endcase
        end
    end
endmodule
