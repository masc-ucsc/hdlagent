module hex_literal_demo (
    output reg [15:0] o
);
  localparam reg [15:0] HexVal = 16'hA55A;  // 16-bit hexadecimal constant
  initial begin
    o = HexVal;
  end
endmodule


