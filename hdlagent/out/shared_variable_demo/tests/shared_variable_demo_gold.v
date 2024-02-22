module shared_variable_demo (
    input  [7:0] a,
    output [7:0] o,
    output [7:0] shared_var
);
  reg [7:0] shared_var;  // This variable is shared between the two blocks
  always @(a) begin
    shared_var = a;
  end
  always @(shared_var) begin
    o = shared_var;
  end
endmodule


