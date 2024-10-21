module Prob140_fsm_hdlc_spec(input [0:0] clk, input [0:0] reset, input [0:0] in, output reg [0:0] disc, output reg [0:0] flag, output reg [0:0] err);
    // State encoding
    localparam ST_IDLE   = 3'b000;
    localparam ST_1      = 3'b001;
    localparam ST_11     = 3'b010;
    localparam ST_111    = 3'b011;
    localparam ST_1111   = 3'b100;
    localparam ST_11111  = 3'b101;
    localparam ST_111110 = 3'b110;
    localparam ST_111111 = 3'b111;
    
    reg [2:0] current_state, next_state;

    // State transition
    always @(posedge clk) begin
        if (reset) begin
            current_state <= ST_IDLE;
        end else begin
            current_state <= next_state;
        end
    end

    // Next state logic
    always @(*) begin
        // Default outputs
        disc = 1'b0;
        flag = 1'b0;
        err  = 1'b0;
        
        case (current_state)
            ST_IDLE: next_state = (in) ? ST_1 : ST_IDLE;
            ST_1: next_state = (in) ? ST_11 : ST_IDLE;
            ST_11: next_state = (in) ? ST_111 : ST_IDLE;
            ST_111: next_state = (in) ? ST_1111 : ST_IDLE;
            ST_1111: next_state = (in) ? ST_11111 : ST_IDLE;
            ST_11111: next_state = (in) ? ST_111110 : ST_11111;
            ST_111110: begin
                next_state = (in) ? ST_111111 : ST_IDLE;
                if (!in) disc = 1'b1;
            end
            ST_111111: begin
                next_state = (in) ? ST_111111 : ST_IDLE;
                if (!in) flag = 1'b1;
                else err = 1'b1;
            end
            default: next_state = ST_IDLE;
        endcase
    end
endmodule
