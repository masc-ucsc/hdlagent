module one_hot_state_register (
    input wire clk,
    input wire rst,
    input wire enable,
    input wire [2:0] state_in,
    output wire [2:0] state_out,
    input wire scan_enable,
    input wire scan_in,
    output wire scan_out
);

shift_register #(
    .WIDTH(3)
) state_reg (
    .clk(clk),
    .rst(rst),
    .enable(enable),
    .data_in(state_in),
    .data_out(state_out),
    .scan_enable(scan_enable),
    .scan_in(scan_in),
    .scan_out(scan_out)
);

endmodule

module shift_register #(
    parameter WIDTH = 8
)(
    input wire clk,
    input wire rst,
    input wire enable,
    input wire [WIDTH-1:0] data_in,
    output wire [WIDTH-1:0] data_out,
    input wire scan_enable,
    input wire scan_in,
    output wire scan_out
);

    reg [WIDTH-1:0] internal_data;

    always @(posedge clk) begin
        if (rst) begin
            internal_data <= {WIDTH{1'b0}};
        end else if (enable) begin
            internal_data <= data_in;
        end else if (scan_enable) begin
            internal_data <= {internal_data[WIDTH-2:0], scan_in};
        end
    end

   assign data_out = internal_data;
    assign scan_out = internal_data[WIDTH-1];

endmodule

