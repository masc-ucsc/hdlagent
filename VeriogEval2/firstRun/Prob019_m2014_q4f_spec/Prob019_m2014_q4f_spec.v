module TopModule(input [0:0] in1, input [0:0] in2, output [0:0] out);
    // AND gate with in2 having an inversion (bubble) at its input
    assign out = in1 & ~in2;
endmodule
