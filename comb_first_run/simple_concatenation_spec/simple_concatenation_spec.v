module simple_concatenation_spec(
    input [7:0] a_i,
    input [7:0] b_i,
    output [15:0] result_o
);

// Concatenate a_i and b_i to form result_o
assign result_o = {a_i, b_i};

endmodule
