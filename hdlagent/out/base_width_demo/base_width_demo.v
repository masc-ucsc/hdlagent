module base_width_demo (
    output reg [7:0] o
);

localparam logic [7:0] constant_value = 8'd170;

always @* begin
    o = constant_value;
end

endmodule