module JKFF_using_DFF (
  input  clk,rst,j,k,
  output q);
  wire t1,t2,t3;

and k2(t1,j,~q);
and k3(t2,~k,q);
or k4(t3,t1,t2);

  DFF d1 (clk,rst,t3,q);
endmodule

module DFF (
  input  clk,rst,d,
  output reg q);

always@(posedge clk)
begin

  if (rst)
    q = 0;
  else
    q = d;

end
endmodule

