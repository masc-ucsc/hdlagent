module alu_spec(input [7:0] A, input [7:0] B, input [3:0] opcode, output [7:0] Y);
    assign Y = (opcode == 4'b0000) ? A + B :                        // Addition
               (opcode == 4'b0001) ? A - B :                        // Subtraction
               (opcode == 4'b0010) ? A & B :                        // Bitwise AND
               (opcode == 4'b0011) ? A | B :                        // Bitwise OR
               (opcode == 4'b0100) ? A ^ B :                        // Bitwise XOR
               (opcode == 4'b0101) ? B << 4 :                       // Left shift B by 4
               (opcode == 4'b0110) ? A << 1 :                       // Left shift A by 1
               (opcode == 4'b0111) ? A >> 1 :                       // Right shift A by 1
               (opcode == 4'b1000) ? {A[6:0], A[7]} :               // Rotate A left
               (opcode == 4'b1001) ? {A[0], A[7:1]} :               // Rotate A right
               (opcode == 4'b1010) ? A - 8'b00000001 :              // Decrement A by 1
               (opcode == 4'b1011) ? ~A :                           // Bitwise NOT of A
               8'b00000000;                                         // Default case: return zero
endmodule
