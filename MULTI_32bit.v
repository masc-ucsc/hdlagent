
module MULTI_32bit(
    input [0:0] clk,
    input [0:0] rst,
    input [31:0] A,
    input [31:0] B,
    output reg [31:0] F
);
    // Internal wires
    wire signA = A[31];
    wire [7:0] expA = A[30:23];
    wire [23:0] mantA = {1'b1, A[22:0]};
    wire signB = B[31];
    wire [7:0] expB = B[30:23];
    wire [23:0] mantB = {1'b1, B[22:0]};
    
    // Sign calculation
    wire resultSign = signA ^ signB;
    
    // Mantissa multiplication and exponent adjustment
    wire [47:0] mantProduct = mantA * mantB;
    wire [15:0] expSum = expA + expB - 8'd127;
    
    // Pipeline registers
    reg [31:0] P1;
    reg [54:0] P2;
    reg [31:0] P3;
    
    // Stage 1: Store sign bit in P1
    always @(posedge clk or posedge rst) begin
        if (rst) P1 <= 32'b0;
        else P1 <= {resultSign, 31'b0};
    end
    
    // Stage 2: Store mantissa product and adjusted exponent in P2
    always @(posedge clk or posedge rst) begin
        if (rst) P2 <= 55'b0;
        else P2 <= {expSum, mantProduct[47:0]};
    end
    
    // Normalization and rounding
    always @(posedge clk or posedge rst) begin
        if (rst) P3 <= 32'b0;
        else begin
            integer shift;
            reg [7:0] adjExp;
            reg [22:0] normMant;
            shift = 0;
            while (!P2[46-shift] && shift < 23) begin
                shift = shift + 1;
            end
            adjExp = P2[54:47] - shift;
            normMant = P2[46-shift:24-shift];
            P3 <= {P1[31], adjExp, normMant};
        end
    end
    
    // Output assignment
    always @(posedge clk) begin
        F <= P3;
    end
endmodule

