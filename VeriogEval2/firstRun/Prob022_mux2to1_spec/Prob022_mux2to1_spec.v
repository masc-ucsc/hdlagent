module TopModule(
    input [0:0] a,
    input [0:0] b,
    input [0:0] sel,
    output [0:0] out
);
    assign out = sel ? b : a; // 2-to-1 multiplexer logic
endmodule
