module latch_with_enable_spec(input [0:0] d, input [0:0] enable, output [0:0] q);
  assign q = (enable) ? d : q;
endmodule
