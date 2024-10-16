module VectorRegFile_spec(
    input logic clk,
    input logic reset,
    input logic [ADDR_WIDTH-1:0] rAddr1_1,
    input logic [ADDR_WIDTH-1:0] rAddr2_1,
    output logic [DATA_WIDTH-1:0] rData1,
    input logic [ADDR_WIDTH-1:0] rAddr1_2,
    input logic [ADDR_WIDTH-1:0] rAddr2_2,
    output logic [DATA_WIDTH-1:0] rData2,
    input logic [ADDR_WIDTH-1:0] wAddr1,
    input logic [ADDR_WIDTH-1:0] wAddr2,
    input logic [DATA_WIDTH-1:0] wData,
    input logic wEnable
);

    parameter ADDR_WIDTH = 5;
    parameter DATA_WIDTH = 32;
    parameter NUM_REG = 16;
    parameter NUM_ELE = 32;

    // Register file array
    logic [DATA_WIDTH-1:0] regfile [0:NUM_REG-1][0:NUM_ELE-1];

    // Asynchronous read process
    assign rData1 = regfile[rAddr1_1][rAddr2_1];
    assign rData2 = regfile[rAddr1_2][rAddr2_2];

    // Synchronous write process
    always_ff @(posedge clk) begin
        if (reset) begin
            // Clear all registers on reset
            for (int i = 0; i < NUM_REG; i = i + 1) begin
                for (int j = 0; j < NUM_ELE; j = j + 1) begin
                    regfile[i][j] <= '0;
                end
            end
        end
        else if (wEnable) begin
            // Write data if wEnable is high
            regfile[wAddr1][wAddr2] <= wData;
        end
    end

endmodule
