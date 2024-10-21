module TopModule(input a, input b, input c, input d, output out);
    assign out = (~a & b & c) | (~a & c & ~d) | (a & ~b & ~c) | (a & ~b & d) | (a & b & c);
endmodule
