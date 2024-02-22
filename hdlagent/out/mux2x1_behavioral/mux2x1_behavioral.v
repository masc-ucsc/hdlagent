module mux2x1_behavioral(
    input [0:0] a,
    input [0:0] b,
    input [0:0] select,
    output reg [0:0] y
);

always @(*) begin
    if (select == 1'b0)
        y = a;
    else
        y = b;
end

endmodule