module TopModule(input [0:0] a, input [0:0] b, input [0:0] c, output [0:0] out);
    assign out = (~a & ~b & c) | (~a & b & ~c) | (~a & b & c) | (a & ~b & ~c) | (a & ~b & c) | (a & b & ~c) | (a & b & c);
endmodule
