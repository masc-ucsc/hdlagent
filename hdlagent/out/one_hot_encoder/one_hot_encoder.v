module one_hot_encoder(
    input [1:0] a,
    output reg [3:0] one_hot
);
always @(*)
    case(a)
        2'b00: one_hot = 4'b0001;
        2'b01: one_hot = 4'b0010;
        2'b10: one_hot = 4'b0100;
        2'b11: one_hot = 4'b1000;
        default: one_hot = 4'b0000;
    endcase
endmodule