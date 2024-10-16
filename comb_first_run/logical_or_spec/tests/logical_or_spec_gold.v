module rorw(
    input [31:0] rs1,
    input [31:0] rs2,
    output reg [31:0] rd
);

wire [4:0] rotate_amount = rs2[4:0];
wire [31:0] rotated_word;

assign rotated_word = (rs1 >> rotate_amount) | (rs1 << (32 - rotate_amount));

always @(*) begin
    rd[31:0] = rotated_word;
end

endmodule

