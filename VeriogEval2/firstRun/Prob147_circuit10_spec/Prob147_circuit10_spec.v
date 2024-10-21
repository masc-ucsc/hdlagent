module TopModule(input clk, input a, input b, output reg q, output reg state);

always @(posedge clk) begin
    state <= a & b ? ~state : b;
    q <= state;
end

endmodule
