module jk_ff_spec(input [0:0] clock, input [0:0] j, input [0:0] k, output [0:0] q, output [0:0] q_bar);
  wire jk;
  assign jk = {j, k};
  
  assign q = (jk == 2'b00) ? q : 
             (jk == 2'b01) ? 1'b0 : 
             (jk == 2'b10) ? 1'b1 : 
             ~q;

  assign q_bar = ~q;
endmodule
