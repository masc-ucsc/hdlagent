module TopModule(
    input [0:0] p1a,
    input [0:0] p1b,
    input [0:0] p1c,
    input [0:0] p1d,
    output [0:0] p1y,
    input [0:0] p2a,
    input [0:0] p2b,
    input [0:0] p2c,
    input [0:0] p2d,
    output [0:0] p2y
);

    // Implementing the first 4-input NAND gate
    assign p1y = ~(p1a & p1b & p1c & p1d);

    // Implementing the second 4-input NAND gate
    assign p2y = ~(p2a & p2b & p2c & p2d);

endmodule
