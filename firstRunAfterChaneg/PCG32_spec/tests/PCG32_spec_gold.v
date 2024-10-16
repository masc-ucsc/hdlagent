module accumulator_microcontroller (
    input wire clk,
    input wire rst,
    input wire scan_enable,
    input wire scan_in,
    output wire scan_out,
    input wire proc_en,
    output wire halt
);
      wire [7:0] alu_A;
    wire [7:0] alu_B;
    wire [7:0] alu_Y;
    wire [4:0] memory_address;
    wire [7:0] memory_data_in;
    wire [7:0] memory_data_out;
    wire [4:0] pc_data_in;
    wire [4:0] pc_data_out;
    wire [7:0] acc_data_in;
    wire [7:0] acc_data_out;
    wire [7:0] ir_data_in;
    wire [7:0] ir_data_out;
    wire cu_PC_write_enable;
    wire [1:0] cu_PC_mux_select;
    wire cu_ACC_write_enable;
    wire [1:0] cu_ACC_mux_select;
    wire cu_IR_load_enable;
    wire [3:0] cu_ALU_opcode;
    wire cu_ALU_inputB_mux_select;
    wire cu_Memory_write_enable;
    wire [1:0] cu_Memory_address_mux_select;
    wire cu_ZF;
    wire control_unit_scan_out;
    wire pc_scan_out;
    wire acc_scan_out;
    wire ir_scan_out;
    wire memory_scan_out;

     alu ALU_inst (
        .A(alu_A),
        .B(alu_B),
        .opcode(cu_ALU_opcode),
        .Y(alu_Y)
    );


    assign alu_A = acc_data_out;

       wire [7:0] immediate;
    assign immediate = {4'b0000, ir_data_out[3:0]};
    assign alu_B = cu_ALU_inputB_mux_select ? immediate : memory_data_out;

    endmodule

module alu(
    input wire [7:0] A,    input wire [7:0] B,
    input wire [3:0] opcode,   output reg [7:0] Y);

     localparam ADD  = 4'b0000;    localparam SUB  = 4'b0001;   localparam AND  = 4'b0010;    localparam OR   = 4'b0011;
    localparam XOR  = 4'b0100;
    localparam NOT  = 4'b0101;   localparam NOP  = 4'b1111;
    always @(A, B, opcode) begin
        case(opcode)
            ADD: Y = A + B;
            SUB: Y = A - B;
            AND: Y = A & B;
            OR:  Y = A | B;
            XOR: Y = A ^ B;
            NOT: Y = ~A;
            NOP: Y = Y;
            default: Y = 8'b00000000;
            endcase
    end

endmodule

