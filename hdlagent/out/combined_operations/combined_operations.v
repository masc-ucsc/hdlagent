module combined_operations (
    input [7:0] a,
    input [7:0] b,
    output reg [7:0] o
);
    
always @* begin
    o = (a & b) ^ (a | b);
end

endmodule