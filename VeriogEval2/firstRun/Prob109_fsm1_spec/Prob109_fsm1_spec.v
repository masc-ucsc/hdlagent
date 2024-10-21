module TopModule (input [0:0] clk, input [0:0] areset, input [0:0] in, output reg [0:0] out);
    typedef enum logic [0:0] {A = 1'b0, B = 1'b1} state_t;
    state_t current_state, next_state;
    
    always_comb begin
        case (current_state)
            B: begin
                out = 1'b1;
                if (in == 1'b0)
                    next_state = A;
                else
                    next_state = B;
            end
            A: begin
                out = 1'b0;
                if (in == 1'b1)
                    next_state = A;
                else
                    next_state = B;
            end
        endcase
    end

    always_ff @(posedge clk or posedge areset) begin
        if (areset)
            current_state <= B;
        else
            current_state <= next_state;
    end
endmodule
