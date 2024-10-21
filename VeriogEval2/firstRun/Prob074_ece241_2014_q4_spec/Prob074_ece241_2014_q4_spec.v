module Prob074_ece241_2014_q4_spec(input [0:0] clk, input [0:0] x, output [0:0] z);
    reg q_xor, q_and, q_or;

    wire xor_input, and_input, or_input;
    wire xor_out, and_out, or_out;

    assign xor_input = x ^ q_xor;
    assign and_input = x & ~q_and;
    assign or_input = x | ~q_or;

    always @(posedge clk) begin
        q_xor <= xor_input;
        q_and <= and_input;
        q_or <= or_input;
    end

    assign z = ~(xor_out ^ and_out ^ or_out);

    assign xor_out = q_xor;
    assign and_out = q_and;
    assign or_out = q_or;
endmodule
