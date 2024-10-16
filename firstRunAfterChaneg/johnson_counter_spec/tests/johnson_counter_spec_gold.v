module d_ff (
    input clock,
    input d,
    output reg q
);
  always @(posedge clock) begin
    q <= d;
  end
endmodule

