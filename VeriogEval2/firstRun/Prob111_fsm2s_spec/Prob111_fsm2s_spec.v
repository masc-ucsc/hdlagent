module Prob111_fsm2s_spec(input [0:0] clk, input [0:0] j, input [0:0] k, input [0:0] reset, output reg [0:0] out);

    // State encoding
    parameter OFF = 1'b0, ON = 1'b1;
    
    reg current_state, next_state;
    
    // State transition logic
    always @(*) begin
        case (current_state)
            OFF: begin
                if (j == 1'b1)
                    next_state = ON;
                else
                    next_state = OFF;
            end
            ON: begin
                if (k == 1'b1)
                    next_state = OFF;
                else
                    next_state = ON;
            end
            default: next_state = OFF;
        endcase
    end

    // State update logic (sequential part)
    always @(posedge clk) begin
        if (reset)
            current_state <= OFF;
        else
            current_state <= next_state;
    end
    
    // Output logic (Moore machine)
    always @(*) begin
        case (current_state)
            OFF: out = 1'b0;
            ON: out = 1'b1;
            default: out = 1'b0;
        endcase
    end

endmodule
