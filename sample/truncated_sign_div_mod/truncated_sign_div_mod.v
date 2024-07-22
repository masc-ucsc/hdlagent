
module truncated_sign_div_mod(
  input signed [7:0] a,
  input signed [7:0] b,
  output signed [5:0] div,
  output signed [5:0] mod
);

  assign div = a/b;
  assign mod = a%b;

endmodule

