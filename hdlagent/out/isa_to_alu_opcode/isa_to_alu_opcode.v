module isa_to_alu_opcode(input [7:0] isa_instr,output reg [3:0] alu_opcode);
always @*
  case(isa_instr[7:4]) // Check the opcode part of the instruction
    4'b1110: alu_opcode = 4'b0000; // ADDI
    4'b0000: alu_opcode = {3'd0, isa_instr[3:0]}; // LDA
    4'b0010: alu_opcode = 4'b0000; // ADD
    4'b0011: alu_opcode = 4'b0001; // SUB
    4'b0100: alu_opcode = 4'b0010; // AND
    4'b0101: alu_opcode = 4'b0011; // OR
    4'b0110: alu_opcode = 4'b0100; // XOR
    4'b1111:                    // Check for the ALU instructions
      case(isa_instr)
        8'b11110110: alu_opcode = 4'b0101; // SHL
        8'b11110111: alu_opcode = 4'b0110; // SHR
        8'b11111000: alu_opcode = 4'b0111; // SHL4
        8'b11111001: alu_opcode = 4'b1000; // ROL
        8'b11111010: alu_opcode = 4'b1001; // ROR
        8'b11111100: alu_opcode = 4'b1010; // DEC
        8'b11111110: alu_opcode = 4'b1011; // INV
        8'b11111101: alu_opcode = 4'b1100; // CLR
        default: alu_opcode = 4'bxxxx; // Undefined opcode
      endcase
    default: alu_opcode = 4'bxxxx; // Undefined opcode
  endcase
endmodule