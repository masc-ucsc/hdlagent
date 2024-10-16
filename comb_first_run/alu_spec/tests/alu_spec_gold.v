module clmul(
    input [31:0] rs1,
    input [31:0] rs2,
    output reg [31:0] rd
);

integer i;

always @(*) begin
    rd = 0;
    for (i = 0; i < 32; i = i + 1) begin
        if ((rs2 >> i) & 1'b1) begin
            rd = rd ^ (rs1 << i);
        end
    end
end

endmodule

