module truncated_sign_div_mod (
    input signed [7:0] a,
    input signed [7:0] b,
    output signed [5:0] div,
    output signed [5:0] mod
);
  wire signed [7:0] full_div;
  wire signed [7:0] full_mod;
  assign full_div = a / b;
  assign full_mod = a % b;
  assign div = full_div[5:0];
  assign mod = full_mod[5:0];
endmodule


