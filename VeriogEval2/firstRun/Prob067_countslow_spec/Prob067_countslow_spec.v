module TopModule(input [0:0] clk, input [0:0] slowena, input [0:0] reset, output reg [3:0] q);

    always @(posedge clk) begin
        if (reset) begin
            q <= 4'b0000; // Reset counter to 0
        end 
        else if (slowena) begin
            if (q == 4'b1001) begin
                q <= 4'b0000; // Wrap around to 0 after reaching 9
            end 
            else begin
                q <= q + 1'b1; // Increment counter
            end
        end
    end

endmodule
