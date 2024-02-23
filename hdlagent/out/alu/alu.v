module alu(
    input [7:0] A,
    input [7:0] B,
    input [3:0] opcode,
    output reg [7:0] Y
);

always @(*) 
begin
    case (opcode)
        4'b0000: Y = B;              // LDA
        4'b0001: Y = A;              // STA
        4'b0010: Y = A + B;          // ADD
        4'b0011: Y = A - B;          // SUB
        4'b0100: Y = A & B;          // AND
        4'b0101: Y = A | B;          // OR
        4'b0110: Y = A ^ B;          // XOR
        4'b1000: Y = A + B;          // ADDI
        4'b1001: Y = ({B,4'b0000});  // LUI
        4'b1010: Y = B;              // SETSEG
        4'b1011: Y = A;              // CSR
        4'b1100: Y = A;              // CSW
        default: Y = 8'b0;            // default case
    endcase
end

endmodule