module biased_sign_compare (
    input signed [7:0] a,
    input signed [7:0] b,
    output out_o
);
  assign out_o = (a + 8'sd4) < b;
endmodule


