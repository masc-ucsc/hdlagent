`define ADDR_WIDTH 4
`define DEPTH 16
`define DATA_WIDTH 8

module async_dualram_16X8 (
    input wire clk,
    input wire rst,
    input wire cs,
    input wire wr_enb,
    input wire [`ADDR_WIDTH-1:0] wr_addr,
    input wire [`DATA_WIDTH-1:0] wr_data,
    input wire rd_enb,
    input wire [`ADDR_WIDTH-1:0] rd_addr,
    output reg [`DATA_WIDTH-1:0] rd_data
);

reg [`DATA_WIDTH-1:0] ram [0:`DEPTH-1];

always @(posedge clk) begin
    if (rst) begin
        integer i;
        for (i = 0; i < `DEPTH; i = i + 1) begin
            ram[i] <= `DATA_WIDTH'd0;
        end
        rd_data <= `DATA_WIDTH'd0;
    end else if (cs) begin
        if (wr_enb) begin
            ram[wr_addr] <= wr_data;
        end
        if (rd_enb) begin
            rd_data <= ram[rd_addr];
        end
    end
end

endmodule



