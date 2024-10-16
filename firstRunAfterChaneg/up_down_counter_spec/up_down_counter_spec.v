module up_down_counter_spec(
    input [0:0] clock,
    input [0:0] reset,
    input [0:0] up_down,
    input [0:0] enable,
    output [3:0] count
);
    reg [3:0] count_reg;

    // Combinational logic to update count_reg
    always @* begin
        if (!reset) begin
            count_reg = 4'b0000;                      // Asynchronous reset, active low
        end else if (enable) begin
            if (up_down) begin
                count_reg = count_reg + 4'b0001;      // Count up
            end else begin
                count_reg = count_reg - 4'b0001;      // Count down
            end
        end
    end

    assign count = count_reg;

endmodule
