module TopModule(input [0:0] a, input [0:0] b, input [0:0] c, input [0:0] d, output [0:0] out);
    // assign output based on the K-map
    assign out = (~a & ~b &  c & ~d) | // ab=00, cd=01
                 (~a & ~b & ~c &  d) | // ab=00, cd=10
                 (~a &  b & ~c & ~d) | // ab=01, cd=00
                 (~a &  b &  c &  d) | // ab=01, cd=11
                 ( a & ~b & ~c &  d) | // ab=10, cd=10
                 ( a & ~b &  c & ~d) | // ab=10, cd=01
                 ( a &  b &  c &  d) | // ab=11, cd=11
                 ( a &  b & ~c & ~d);  // ab=11, cd=01
endmodule
