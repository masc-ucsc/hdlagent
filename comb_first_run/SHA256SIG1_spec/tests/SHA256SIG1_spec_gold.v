module rev8(
    input [31:0] rs,
    output reg [31:0] rd
);

always @(rs) begin
    rd = {rs[7:0], rs[15:8], rs[23:16], rs[31:24]};
end

endmodule

