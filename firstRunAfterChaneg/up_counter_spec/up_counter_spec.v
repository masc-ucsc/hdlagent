module up_counter_spec(input [0:0] clock, input [0:0] reset, output reg [1:0] count);
    always @(*) begin
        if (reset) begin
            count = 2'b00; // Reset to 0
        end else begin
            count = count + 1; // Increment count
        end
    end
endmodule
