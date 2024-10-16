module counter_spec(
    input [0:0] CE,
    input [0:0] UpDown,
    input [0:0] reset,
    input [0:0] clock,
    output reg [7:0] CountOut
);

    always @(posedge clock) begin
        if (reset)
            CountOut <= 8'b00000000; // Synchronous reset
        else if (CE) begin
            if (UpDown)
                CountOut <= CountOut + 1; // Increment when UpDown = 1
            else
                CountOut <= CountOut - 1; // Decrement when UpDown = 0
        end
    end

endmodule
