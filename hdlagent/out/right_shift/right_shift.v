module right_shift (
    input [7:0] a,
    output [7:0] o
);

assign o = {a[5:0], 2'b0};

endmodule