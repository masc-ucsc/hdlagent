module constant_demo (
    output reg [7:0] o
);

localparam constant_value = 8'b10101010;

always @* begin
    o = constant_value;
end

endmodule