module TopModule(input [0:0] clk, input [0:0] d, input [0:0] r, output [0:0] logic q);
    assign q = (r) ? 1'b0 : d;
endmodule
