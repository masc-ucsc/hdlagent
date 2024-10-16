module voting_machine_spec(
    input [0:0] clk,
    input [0:0] rst,
    input [0:0] i_candidate_1,
    input [0:0] i_candidate_2,
    input [0:0] i_candidate_3,
    input [0:0] i_voting_over,
    output reg [31:0] o_count1,
    output reg [31:0] o_count2,
    output reg [31:0] o_count3
);
    
    // State declaration
    typedef enum logic [1:0] {IDLE, VOTE, HOLD, FINISH} state_t;
    state_t current_state, next_state;
    
    reg [15:0] debounce_counter; // 16-bit counter for debounce handling
    reg prev_vote1, prev_vote2, prev_vote3; // Previous vote states
    
    // Transition between states
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            current_state <= IDLE;
            o_count1 <= 32'd0;
            o_count2 <= 32'd0;
            o_count3 <= 32'd0;
            debounce_counter <= 16'd0;
            prev_vote1 <= 1'b0;
            prev_vote2 <= 1'b0;
            prev_vote3 <= 1'b0;
        end else begin
            current_state <= next_state;
            
            // Debounce logic and vote counting
            if (current_state == VOTE) begin
                if (!prev_vote1 && i_candidate_1) o_count1 <= o_count1 + 1'b1;
                if (!prev_vote2 && i_candidate_2) o_count2 <= o_count2 + 1'b1;
                if (!prev_vote3 && i_candidate_3) o_count3 <= o_count3 + 1'b1;
            end
            
            // Update previous vote states
            if (current_state == VOTE || current_state == HOLD) begin
                prev_vote1 <= i_candidate_1;
                prev_vote2 <= i_candidate_2;
                prev_vote3 <= i_candidate_3;
            end
            
            // Manage debounce counter
            if (current_state == HOLD) begin
                debounce_counter <= debounce_counter + 16'd1;
            end else begin
                debounce_counter <= 16'd0;
            end
        end
    end

    // Determine next state
    always @* begin
        case (current_state)
            IDLE: begin
                next_state = (i_voting_over) ? FINISH : VOTE;
            end
            VOTE: begin
                if (i_voting_over) begin
                    next_state = FINISH;
                end else if (i_candidate_1 || i_candidate_2 || i_candidate_3) begin
                    next_state = HOLD;
                end else begin
                    next_state = VOTE;
                end
            end
            HOLD: begin
                next_state = (debounce_counter == 16'hFFFF) ? VOTE : HOLD; // Wait for debounce
            end
            FINISH: begin
                next_state = FINISH; // Remain in FINISH state
            end
            default: begin
                next_state = IDLE;
            end
        endcase
    end
endmodule
