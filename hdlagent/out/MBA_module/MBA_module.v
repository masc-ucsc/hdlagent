module MBA_module( 
  output  [15:0] p,
  input  [7:0] a,
  input  [7:0] b
); 
  // Combinational multiplier 
  assign p = a * b;
endmodule