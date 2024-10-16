module jk_ff (
    input  clock,
    input  j,
    input k,
    output q,
    output q_bar
);
  reg q_reg;
  always @(posedge clock) begin
    if (j && !k) q_reg <= 1;
    else if (!j && k) q_reg <= 0;
    else if (j && k) q_reg <= ~q_reg;
  end
  assign q = q_reg;
  assign q_bar = ~q_reg;
endmodule

