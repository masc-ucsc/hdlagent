module Prob110_fsm2_spec(
    input [0:0] clk,
    input [0:0] j,
    input [0:0] k,
    input [0:0] areset,
    output reg [0:0] out
);

    // State Encoding
    parameter OFF = 1'b0, ON = 1'b1;
    reg state, next_state;

    // Next state logic
    always @(*) begin
        case (state)
            OFF: next_state = j ? ON : OFF;
            ON:  next_state = k ? OFF : ON;
            default: next_state = OFF;
        endcase
    end

    // State register with asynchronous reset
    always @(posedge clk or posedge areset) begin
        if (areset) 
            state <= OFF;
        else 
            state <= next_state;
    end

    // Output logic
    always @(*) begin
        out = (state == ON) ? 1'b1 : 1'b0;
    end

endmodule
