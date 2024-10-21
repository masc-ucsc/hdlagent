module Prob082_lfsr32_spec(input [0:0] clk, input [0:0] reset, output reg [31:0] q);
    wire feedback = q[31] ^ q[21] ^ q[1] ^ q[0];
    
    always @(posedge clk) begin
        if (reset) begin
            q <= 32'h00000001; // Reset to the value 32'h1
        end else begin
            q <= {q[30:0], feedback}; // Shift left and insert feedback bit
        end
    end
endmodule
