module latch_with_enable (
    input  d,
    input  enable,
    output q
);
  reg q_reg;
  always @(d, enable) begin
    if (enable) q_reg = d;
  end
  assign q = q_reg;
endmodule

