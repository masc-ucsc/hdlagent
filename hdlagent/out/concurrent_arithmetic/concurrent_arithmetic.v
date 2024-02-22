module concurrent_arithmetic(
    input [3:0] a,
    input [3:0] b,
    output reg [3:0] sum,
    output reg [3:0] diff
);

always @(*) begin
    sum = a + b;
    diff = a - b;
end

endmodule