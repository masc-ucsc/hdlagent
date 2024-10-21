module TopModule(input clk, input aresetn, input x, output reg z);
    reg [1:0] state, next_state;

    // State encoding
    localparam S0 = 2'b00; // initial state
    localparam S1 = 2'b01; // state after detecting '1'
    localparam S2 = 2'b10; // state after detecting '10'

    // State transition on positive edge of clock
    always @(posedge clk or negedge aresetn) begin
        if (!aresetn)
            state <= S0;
        else
            state <= next_state;
    end

    // Next state and output logic
    always @(*) begin
        case (state)
            S0: begin
                if (x)
                    next_state = S1;
                else
                    next_state = S0;
                z = 0;
            end
            S1: begin
                if (x)
                    next_state = S1;
                else
                    next_state = S2;
                z = 0;
            end
            S2: begin
                if (x) begin
                    next_state = S1;
                    z = 1;
                end else begin
                    next_state = S0;
                    z = 0;
                end
            end
            default: begin
                next_state = S0;
                z = 0;
            end
        endcase
    end
endmodule
