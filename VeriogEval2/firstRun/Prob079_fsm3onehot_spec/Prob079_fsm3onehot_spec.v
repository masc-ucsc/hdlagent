module TopModule(input [0:0] in, input [3:0] state, output [3:0] next_state, output [0:0] out);
    // Define next state logic
    assign next_state[0] = state[2] & ~in; // A
    assign next_state[1] = (state[0] | state[1]) & ~in | state[3] & in; // B
    assign next_state[2] = (state[1] & in) | (state[3] & ~in); // C
    assign next_state[3] = state[2] & in; // D
    
    // Define output logic
    assign out = state[3]; // Output is '1' only in state D
endmodule
