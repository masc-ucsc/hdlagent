module Prob127_lemmings1_spec(
    input [0:0] clk, 
    input [0:0] areset, 
    input [0:0] bump_left, 
    input [0:0] bump_right, 
    output reg [0:0] walk_left, 
    output reg [0:0] walk_right
);

    reg state, next_state;
    
    // State encoding
    localparam WALK_LEFT = 1'b0;
    localparam WALK_RIGHT = 1'b1;
    
    // State transition logic
    always @(*) begin
        case (state)
            WALK_LEFT: begin
                if (bump_left) 
                    next_state = WALK_RIGHT;
                else 
                    next_state = WALK_LEFT;
            end
            WALK_RIGHT: begin
                if (bump_right)
                    next_state = WALK_LEFT;
                else 
                    next_state = WALK_RIGHT;
            end
            default: next_state = WALK_LEFT;
        endcase
    end

    // State flip-flops with asynchronous reset
    always @(posedge clk or posedge areset) begin
        if (areset)
            state <= WALK_LEFT;
        else
            state <= next_state;
    end

    // Output logic
    always @(*) begin
        case (state)
            WALK_LEFT: begin
                walk_left = 1'b1;
                walk_right = 1'b0;
            end
            WALK_RIGHT: begin
                walk_left = 1'b0;
                walk_right = 1'b1;
            end
        endcase
    end

endmodule
