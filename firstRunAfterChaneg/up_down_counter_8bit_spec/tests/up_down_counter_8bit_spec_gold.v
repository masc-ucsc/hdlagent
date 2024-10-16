module concurrent_toggles (
    input clock,
    input reset,
    output reg a,
    output reg b
);
  always @(posedge clock) begin
 if (reset) begin
 a <= 0; end
else begin a <= ~a; end end
  always @(posedge clock) begin
if (reset) begin
 b <= 0; end else
 begin b <= ~b; end end
endmodule

