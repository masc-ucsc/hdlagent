module TopModule(input [0:0] a, input [0:0] b, output [0:0] out);
    assign out = ~(a ^ b); // XNOR logic
endmodule
