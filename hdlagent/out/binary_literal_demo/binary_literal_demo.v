module binary_literal_demo (
    input [3:0] a,
    output o
);
assign o = (a == 4'b1011) ? 1'b1 : 1'b0;
endmodule