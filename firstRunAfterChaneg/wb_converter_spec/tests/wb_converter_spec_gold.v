module Predicate_Register_File(
    input logic clk,
    input logic reset,
    input logic [3:0] read_addr,  // 4 bits to address 16 registers
    input logic [3:0] write_addr,
    input logic write_enable,
    input logic data_in,
    output logic data_out
);

// Explicitly declaring each 1-bit register
logic reg0, reg1, reg2, reg3, reg4, reg5, reg6, reg7,
     reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15;

// Write logic
always_ff @(posedge clk or posedge reset) begin
    if (reset) begin
        reg0 <= 0; reg1 <= 0; reg2 <= 0; reg3 <= 0;
        reg4 <= 0; reg5 <= 0; reg6 <= 0; reg7 <= 0;
        reg8 <= 0; reg9 <= 0; reg10 <= 0; reg11 <= 0;
        reg12 <= 0; reg13 <= 0; reg14 <= 0; reg15 <= 0;
    end else if (write_enable) begin
        case (write_addr)
            4'd0: reg0 <= data_in;
            4'd1: reg1 <= data_in;
            4'd2: reg2 <= data_in;
            4'd3: reg3 <= data_in;
            4'd4: reg4 <= data_in;
            4'd5: reg5 <= data_in;
            4'd6: reg6 <= data_in;
            4'd7: reg7 <= data_in;
            4'd8: reg8 <= data_in;
            4'd9: reg9 <= data_in;
            4'd10: reg10 <= data_in;
            4'd11: reg11 <= data_in;
            4'd12: reg12 <= data_in;
            4'd13: reg13 <= data_in;
            4'd14: reg14 <= data_in;
            4'd15: reg15 <= data_in;
        endcase
    end
end

// Read logic
always_comb begin
    case (read_addr)
        4'd0: data_out = reg0;
        4'd1: data_out = reg1;
        4'd2: data_out = reg2;
        4'd3: data_out = reg3;
        4'd4: data_out = reg4;
        4'd5: data_out = reg5;
        4'd6: data_out = reg6;
        4'd7: data_out = reg7;
        4'd8: data_out = reg8;
        4'd9: data_out = reg9;
        4'd10: data_out = reg10;
        4'd11: data_out = reg11;
        4'd12: data_out = reg12;
        4'd13: data_out = reg13;
        4'd14: data_out = reg14;
        4'd15: data_out = reg15;
        default: data_out = 0; // Fallback case
    endcase
end

endmodule

