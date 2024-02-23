module isa_to_alu_opcode (
    input [7:0] isa_instr,
    output reg [3:0] alu_opcode
);


    wire [7:0] opcode_8bit = isa_instr[7:0];
    wire [3:0] opcode_4bit = isa_instr[7:4];
    wire [2:0] opcode_3bit = isa_instr[7:5];

    always @* begin
        case (opcode_8bit)
            8'b11110110: alu_opcode = 4'b0101;
            8'b11110111: alu_opcode = 4'b0110;
            8'b11111000: alu_opcode = 4'b0111;
            8'b11111001: alu_opcode = 4'b1000;
            8'b11111010: alu_opcode = 4'b1001;
            8'b11111100: alu_opcode = 4'b1010;
            8'b11111110: alu_opcode = 4'b1011;
            8'b11111101: alu_opcode = 4'b1100;

            default: begin
                case (opcode_4bit)
                    4'b1110: alu_opcode = 4'b0000;

                    default: begin
                        case (opcode_3bit)
                            3'b010: alu_opcode = 4'b0000;
                            3'b011: alu_opcode = 4'b0001;
                            3'b100: alu_opcode = 4'b0010;
                            3'b101: alu_opcode = 4'b0011;
                            3'b110: alu_opcode = 4'b0100;

                            default: alu_opcode = 4'b0000;
                        endcase
                    end
                endcase
            end
        endcase
    end

endmodule





