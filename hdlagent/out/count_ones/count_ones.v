module count_ones (
    input [3:0] a,
    output [1:0] count
);

assign count = {(a[3] & ~a[2]), (a[2] & ~a[1]) | (a[1] & ~a[0])};

endmodule