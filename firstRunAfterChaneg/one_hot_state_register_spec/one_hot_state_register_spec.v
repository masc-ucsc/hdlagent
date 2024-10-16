module one_hot_state_register_spec(
    input [0:0] clk,
    input [0:0] rst,
    input [0:0] enable,
    input [2:0] state_in,
    output [2:0] state_out,
    input [0:0] scan_enable,
    input [0:0] scan_in,
    output [0:0] scan_out
);

    reg [2:0] state_reg;
    reg scan_out_reg;

    always @(*) begin
        if (rst) begin
            state_reg = 3'b001; // Default to FETCH state on reset
        end else if (scan_enable) begin
            state_reg = {state_reg[1:0], scan_in}; // Scan chain shift
        end else if (enable) begin
            state_reg = state_in; // Load input state
        end
        // No else needed, state retains its value when no control signals are active
    end

    assign state_out = state_reg;
    assign scan_out = state_reg[2]; // Output the last bit for scan chain

endmodule
