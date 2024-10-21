module Prob063_review2015_shiftcount_spec(
    input [0:0] clk,
    input [0:0] shift_ena,
    input [0:0] count_ena,
    input [0:0] data,
    output reg [3:0] q
);
    
    always @(posedge clk) begin
        if (shift_ena) begin
            q <= {data, q[3:1]}; // Shift in data at MSB
        end else if (count_ena) begin
            q <= q - 1; // Decrement counter
        end
    end

endmodule
