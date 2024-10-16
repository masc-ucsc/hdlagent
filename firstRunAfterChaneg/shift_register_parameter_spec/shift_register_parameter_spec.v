module shift_register_parameter_spec #(parameter WIDTH = 8)(
    input [0:0] clk,
    input [0:0] rst,
    input [0:0] enable,
    input [WIDTH-1:0] data_in,
    output reg [WIDTH-1:0] data_out,
    input [0:0] scan_enable,
    input [0:0] scan_in,
    output [0:0] scan_out
);

    reg [WIDTH-1:0] shift_reg;

    always @(posedge clk or posedge rst) begin
        if (rst)
            shift_reg <= {WIDTH{1'b0}};
        else if (enable)
            shift_reg <= data_in;
        else if (scan_enable)
            shift_reg <= {shift_reg[WIDTH-2:0], scan_in};
    end

    assign data_out = shift_reg;
    assign scan_out = shift_reg[WIDTH-1];

endmodule
