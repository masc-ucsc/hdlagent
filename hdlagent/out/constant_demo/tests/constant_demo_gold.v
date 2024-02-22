module constant_demo (
    output reg [7:0] o
);
  localparam reg [7:0] ConstanVal = 8'b10101010;
  initial begin
    o = ConstanVal;
  end
endmodule


