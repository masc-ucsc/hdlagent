module async_jk_ff_spec(input [0:0] clock, input [0:0] reset, input [0:0] j, input [0:0] k, output [0:0] q);
    wire q_int; // Internal wire for holding the state

    assign q_int = (~reset) ? 1'b0 : // Asynchronous active-low reset
                   (j & ~k & ~q)    ? 1'b1 : // Flip to 1
                   (~j & k & q)     ? 1'b0 : // Flip to 0
                   (j & k)          ? ~q : // Toggle
                                      q; // No change

    assign q = q_int;

endmodule
