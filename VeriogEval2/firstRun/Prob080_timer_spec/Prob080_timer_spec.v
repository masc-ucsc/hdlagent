module TopModule(
    input [0:0] clk,
    input [0:0] load,
    input [9:0] data,
    output [0:0] tc
);

reg [9:0] counter;
reg tc_reg;

// Combinational logic to determine the terminal count output
assign tc = tc_reg;

always @(posedge clk) begin
    if (load) begin
        counter <= data; // Load the counter
    end else if (counter != 0) begin
        counter <= counter - 1; // Decrement the counter
    end

    // Update terminal count signal
    if (counter == 0) begin
        tc_reg <= 1;
    end else begin
        tc_reg <= 0;
    end
end

endmodule
