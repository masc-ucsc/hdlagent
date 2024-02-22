module alu(
    input [7:0] A,
    input [7:0] B,
    input [4:0] opcode,
    output reg [7:0] Y
); 

always @* begin // Combinational logic
    // Default value for Y
    Y = 8'b0;
    
    case(opcode)
        4'b0000: Y = A; // Load accumulator A
        4'b0001: Y = B; // Store accumulator A
        4'b0010: Y = A + B; // Adding A and B
        4'b0011: Y = A - B; // Subtracting B from A
        4'b0100: Y = A & B; // AND operation
        4'b0101: Y = A | B; // OR operation
        4'b0110: Y = A ^ B; // XOR operation
        4'b1000: Y = A + B; // Add immediate to A
        4'b1001: Y = {B[3:0], 4'b0000}; // Load upper immediate
        4'b1010: Y = B; // Set SEGMENT
        4'b1011: Y = A; // Read CSR to Accumulator 
        4'b1100: Y = A; // Write to CSR from Accumulator 
        default: Y = 8'b0; // Default case
    endcase
end

endmodule