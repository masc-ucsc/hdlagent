module local_variable_demo (
    input  [ 7:0] a,
    output [15:0] o,
    output [ 0:0] is_even
);
  reg is_even;  // This is a local variable
  always @(a) begin
    is_even = a[0] == 0;
  end
  assign o = is_even;
endmodule


