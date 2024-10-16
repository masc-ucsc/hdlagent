module alu (
    input wire [7:0] A,
    input wire [7:0] B,
    input wire [3:0] opcode,
    output reg [7:0] Y
);

always @(*) begin
    case (opcode)
        4'b0000: Y = A + B;
        4'b0001: Y = A - B;
        4'b0010: Y = A & B;
        4'b0011: Y = A | B;
        4'b0100: Y = A ^ B;
        4'b0101: Y = B << 4;
        4'b0110: Y = A << 1;
        4'b0111: Y = A >> 1;
        4'b1000: Y = A[6:0] | A[7] << 7;
        4'b1001: Y = A[0] << 7 | A[7:1];
        4'b1010: Y = A - 1;
        4'b1011: Y = ~A;
        default: Y = 8'b00000000;
    endcase
end

endmodule

