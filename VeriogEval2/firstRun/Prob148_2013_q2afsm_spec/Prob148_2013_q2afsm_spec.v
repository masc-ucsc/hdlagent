module Prob148_2013_q2afsm_spec(input [0:0] clk, input [0:0] resetn, input [2:0] r, output reg [2:0] g);

    // State encoding
    parameter A = 2'b00, B = 2'b01, C = 2'b10;

    reg [1:0] current_state, next_state;

    // State flip-flops (sequential logic)
    always @(posedge clk or negedge resetn) begin
        if (!resetn)
            current_state <= A; // Reset condition
        else
            current_state <= next_state;
    end

    // Next state logic (combinational logic)
    always @(*) begin
        case (current_state)
            A: begin
                if (r[0])
                    next_state = B;
                else if (r[1])
                    next_state = C;
                else
                    next_state = A;
            end
            B: begin
                if (r[0])
                    next_state = B;
                else
                    next_state = A;
            end
            C: begin
                if (r[1])
                    next_state = C;
                else
                    next_state = A;
            end
            default: next_state = A;
        endcase
    end

    // Output logic (combinational logic)
    always @(*) begin
        g = 3'b000; // Default output
        case (current_state)
            B: g[0] = 1'b1; // State B: g0 = 1
            C: g[1] = 1'b1; // State C: g1 = 1
            default: g = 3'b000;
        endcase
    end

endmodule
