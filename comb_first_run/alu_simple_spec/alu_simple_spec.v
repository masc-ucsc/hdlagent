module alu_simple_spec(input [7:0] A, input [7:0] B, input [3:0] opcode, output reg [7:0] Y);
    always @(*) begin
        case(opcode)
            4'b0000: Y = A + B;               // Addition
            4'b0001: Y = A - B;               // Subtraction
            4'b0010: Y = A & B;               // Bitwise AND
            4'b0011: Y = A | B;               // Bitwise OR
            4'b0100: Y = A ^ B;               // Bitwise XOR
            4'b0101: Y = B << 4;              // Shift B left by 4
            4'b0110: Y = A << 1;              // Shift A left by 1
            4'b0111: Y = A >> 1;              // Shift A right by 1
            4'b1000: Y = {A[6:0], A[7]};      // Rotate A left
            4'b1001: Y = {A[0], A[7:1]};      // Rotate A right
            4'b1010: Y = A - 1;               // Decrement A by 1
            4'b1011: Y = ~A;                  // Invert all bits of A
            default: Y = 8'b00000000;         // Default case: Y = 0
        endcase
    end
endmodule
