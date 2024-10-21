module Prob049_m2014_q4b_spec(input [0:0] clk, input [0:0] d, input [0:0] ar, output logic [0:0] q);
    always @ (posedge clk or posedge ar) begin
        if (ar)
            q <= 0; // asynchronous reset
        else
            q <= d; // D flip-flop behavior
    end
endmodule
