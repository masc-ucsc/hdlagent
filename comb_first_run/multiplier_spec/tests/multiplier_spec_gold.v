module hex_literal_demo (
    output reg [15:0] o
);
  localparam reg [15:0] HexVal = 16'hA55A;
  initial begin
    o = HexVal;
  end
endmodule

