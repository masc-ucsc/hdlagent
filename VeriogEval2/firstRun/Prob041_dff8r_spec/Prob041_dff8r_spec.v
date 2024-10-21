module TopModule(input [0:0] clk, input [7:0] d, input [0:0] reset, output [7:0] q);

    reg [7:0] q_reg;

    always @(posedge clk) begin
        if (reset) 
            q_reg <= 8'b0; // Synchronous reset
        else
            q_reg <= d;
    end

    assign q = q_reg;

endmodule
