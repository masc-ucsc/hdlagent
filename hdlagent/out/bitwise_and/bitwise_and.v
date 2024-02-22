module bitwise_and (
    input [7:0] a,
    input [7:0] b,
    output reg [7:0] o
);
    always @* begin
        o = a & b;
    end
endmodule