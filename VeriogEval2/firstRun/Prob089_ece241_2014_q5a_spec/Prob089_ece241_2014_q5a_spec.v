module TopModule(input clk, input areset, input x, output reg z);

// State Declaration
typedef enum logic [1:0] {
    S0 = 2'b00,  // Initial state
    S1 = 2'b01   // State after first 1 has been encountered
} state_t;

// State Register
state_t current_state, next_state;

// Combinational Logic for State Transition
always @(*) begin
    case (current_state)
        S0: 
            if (x)
                next_state = S1;
            else
                next_state = S0;
        S1: 
            next_state = S1;  // Remain in S1 once entered
        default: 
            next_state = S0;  // Default to S0
    endcase
end

// Output Logic based on Moore Machine
always @(*) begin
    case (current_state)
        S0: z = x;          // Output same as input
        S1: z = ~x;         // Complement the input
        default: z = 1'b0;  // Default output
    endcase
end

// Sequential Logic for State Update
always @(posedge clk or posedge areset) begin
    if (areset)
        current_state <= S0;  // Reset state to S0
    else
        current_state <= next_state;  // Update state
end

endmodule
