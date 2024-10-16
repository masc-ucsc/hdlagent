module VectorRegFile #(
    parameter ADDR_WIDTH = 5,
    parameter DATA_WIDTH = 32,
    parameter NUM_REG = 4,
    parameter NUM_ELE = 4
)(
    input logic clk,
    input logic reset,
    input logic [ADDR_WIDTH-1:0] rAddr1_1, rAddr2_1,
    output logic [DATA_WIDTH-1:0] rData1,
    input logic [ADDR_WIDTH-1:0] rAddr1_2, rAddr2_2,
    output logic [DATA_WIDTH-1:0] rData2,
    input logic [ADDR_WIDTH-1:0] wAddr1, wAddr2,
    input logic [DATA_WIDTH-1:0] wData,
    input logic wEnable
);

    logic [DATA_WIDTH-1:0] reg0, reg1, reg2, reg3,
                            reg4, reg5, reg6, reg7,
                            reg8, reg9, reg10, reg11,
                            reg12, reg13, reg14, reg15;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            reg0 <= 0; reg1 <= 0; reg2 <= 0; reg3 <= 0;
            reg4 <= 0; reg5 <= 0; reg6 <= 0; reg7 <= 0;
            reg8 <= 0; reg9 <= 0; reg10 <= 0; reg11 <= 0;
            reg12 <= 0; reg13 <= 0; reg14 <= 0; reg15 <= 0;
        end else if (wEnable) begin
                     case ({wAddr1, wAddr2})
                4'b0000: reg0 <= wData;
                4'b0001: reg1 <= wData;
                4'b0010: reg2 <= wData;
                4'b0011: reg3 <= wData;
                4'b0100: reg4 <= wData;
                4'b0101: reg5 <= wData;
                4'b0110: reg6 <= wData;
                4'b0111: reg7 <= wData;
                4'b1000: reg8 <= wData;
                4'b1001: reg9 <= wData;
                4'b1010: reg10 <= wData;
                4'b1011: reg11 <= wData;
                4'b1100: reg12 <= wData;
                4'b1101: reg13 <= wData;
                4'b1110: reg14 <= wData;
                4'b1111: reg15 <= wData;
            endcase
        end
    end

    always_comb begin
             case ({rAddr1_1, rAddr2_1})
            4'b0000: rData1 = reg0;
            4'b0001: rData1 = reg1;
                      4'b1111: rData1 = reg15;
            default: rData1 = 0;
        endcase

        case ({rAddr1_2, rAddr2_2})
            4'b0000: rData2 = reg0;
            4'b0001: rData2 = reg1;
                 4'b1111: rData2 = reg15;
            default: rData2 = 0;
        endcase
    end
endmodule

