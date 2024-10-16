module four_bit_sync_counter_spec(input [0:0] clock, input [0:0] reset, output [3:0] out_o);
    wire [3:0] next_state;
    reg [3:0] state;

    // D Flip-Flops for each bit of the counter state
    always @(posedge clock or posedge reset) begin
        if (reset) begin
            state <= 4'b0000; // Reset the counter to 0
        end else begin
            state <= next_state; // Update state to next state
        end
    end

    // Combinational logic to generate next state
    assign next_state = state + 1;

    // Output the current state
    assign out_o = state;
endmodule
