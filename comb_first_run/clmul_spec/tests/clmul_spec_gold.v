module SHA256SIG1(
    input [31:0] rs1,
    output reg [31:0] rd
);

function [31:0] ror32;
    input [31:0] value;
    input integer bits;
    begin
        ror32 = (value >> bits) | (value << (32 - bits));
    end
endfunction

wire [31:0] rotate_right_17;
wire [31:0] rotate_right_19;
wire [31:0] shift_right_10;
wire [31:0] result;

assign rotate_right_17 = ror32(rs1, 17);
assign rotate_right_19 = ror32(rs1, 19);
assign shift_right_10 = rs1 >> 10;

assign result = rotate_right_17 ^ rotate_right_19 ^ shift_right_10;

always @(rs1) begin
    rd <= result;
end

endmodule

