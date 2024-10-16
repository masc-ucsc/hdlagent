module shift_register_param_spec
    #(parameter WIDTH = 8)
    (
    input [0:0] clk,
    input [0:0] rst,
    input [0:0] enable,
    input [WIDTH-1:0] data_in,
    output reg [WIDTH-1:0] data_out,
    input [0:0] scan_enable,
    input [0:0] scan_in,
    output [0:0] scan_out
    );

    always @(*) begin
        if (rst) begin
            // Reset the register
            data_out = {WIDTH{1'b0}};
        end else if (scan_enable) begin
            // Shift register with scan chain functionality
            data_out = {data_out[WIDTH-2:0], scan_in};
        end else if (enable) begin
            // Load new data
            data_out = data_in;
        end
    end

    // Provide scan_output as last bit of current data_out
    assign scan_out = data_out[WIDTH-1];

endmodule
