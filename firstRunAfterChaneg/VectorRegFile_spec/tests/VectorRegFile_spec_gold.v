module MULTI_32bit(
    input clk,
    input rst,
    input [31:0] A,
    input [31:0] B,
    output reg [31:0] F
);

reg [31:0] P1, P2, P3;
wire signA, signB;
assign signA = A[31];
assign signB = B[31];
wire [7:0] expA, expB;
assign expA = A[30:23];
assign expB = B[30:23];
wire [23:0] mantA, mantB;
assign mantA = {1'b1, A[22:0]};
assign mantB = {1'b1, B[22:0]};
parameter bias = 8'd127;
wire [47:0] mantProduct;
wire [15:0] expSum;
wire signProduct;
assign mantProduct = mantA * mantB;
assign expSum = expA + expB - bias;
assign signProduct = signA ^ signB;

always @(posedge clk or posedge rst) begin
    if (rst) P1 <= 32'd0;
    else P1 <= {signProduct, 31'd0};
end

always @(posedge clk or posedge rst) begin
    if (rst) P2 <= 32'd0;
    else P2 <= {P1[31], expSum[7:0], mantProduct[46:24]};
end

always @(posedge clk or posedge rst) begin
    if (rst) P3 <= 32'd0;
    else P3 <= P2;
end

always @(posedge clk or posedge rst) begin
    if (rst) F <= 32'd0;
    else F <= P3;
end

endmodule

