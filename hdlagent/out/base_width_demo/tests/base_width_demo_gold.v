module base_width_demo (
    output reg [7:0] o
);

  localparam reg [7:0] ConstantVal = 8'd170;  // 8-bit decimal constant 170 is binary 10101010

  initial begin
    o = ConstantVal;
  end

endmodule


