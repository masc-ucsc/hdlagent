module SHA256SIG1_spec(input [31:0] rs1, output [31:0] rd);

  // Rotate right 32 bits by n
  function [31:0] ror32;
    input [31:0] data;
    input [4:0] n;
    begin
      ror32 = (data >> n) | (data << (32 - n));
    end
  endfunction

  wire [31:0] ror17;
  wire [31:0] ror19;
  wire [31:0] shr10;

  // Compute rotations and shift
  assign ror17 = ror32(rs1, 17);
  assign ror19 = ror32(rs1, 19);
  assign shr10 = rs1 >> 10;

  // Compute final result
  assign rd = ror17 ^ ror19 ^ shr10;

endmodule
