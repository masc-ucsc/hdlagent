module async_jk_ff (
    input clock,
    input reset,
    input j,
    input k,
    output reg q
);
  always @(posedge clock or negedge reset) begin
    if (!reset) q <= 0;
    else if (j && !k) q <= 1;
    else if (!j && k) q <= 0;
    else if (j && k) q <= ~q;
  end
endmodule

