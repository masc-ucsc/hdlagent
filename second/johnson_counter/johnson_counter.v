module johnson_counter(input [0:0] clock, input [0:0] reset, output reg [3:0] q);

wire [3:0] next_state;
assign next_state = {q[0], q[3:1]}; // Logic for next state generation

always @(posedge clock or posedge reset) begin
    if (reset) begin
        q <= 4'b0001; // Reset state
    end else begin
        q <= next_state; // Assign next state on clock edge
    end
end

endmodule
