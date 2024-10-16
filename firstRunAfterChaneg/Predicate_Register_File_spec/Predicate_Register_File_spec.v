module Predicate_Register_File_spec(
    input [0:0] logic clk,
    input [0:0] logic reset,
    input [0:0] logic [3:0] read_addr,
    input [0:0] logic [3:0] write_addr,
    input [0:0] logic write_enable,
    input [0:0] logic data_in,
    output [0:0] logic data_out
);

    logic [15:0] registers;

    // Combinational read
    assign data_out = registers[read_addr];

    // Sequential write and reset
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            registers <= 16'b0; // Clear all registers
        end else if (write_enable) begin
            registers[write_addr] <= data_in; // Write data_in to selected register
        end
    end

endmodule
