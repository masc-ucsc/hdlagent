module TopModule(input [0:0] clk, input [7:0] in, input [0:0] reset, output [0:0] done);
    reg [1:0] state, next_state;
    reg [0:0] done_reg;
    
    // State Encoding
    localparam IDLE = 2'b00;
    localparam BYTE_1 = 2'b01;
    localparam BYTE_2 = 2'b10;
    localparam BYTE_3 = 2'b11;

    // Combinational logic for next state and output
    always @(*) begin
        next_state = state;
        done_reg = 1'b0;
        case (state)
            IDLE: begin
                if (in[3] == 1'b1)
                    next_state = BYTE_1;
            end
            BYTE_1: begin
                next_state = BYTE_2;
            end
            BYTE_2: begin
                next_state = BYTE_3;
            end
            BYTE_3: begin
                done_reg = 1'b1; // Signal done
                if (in[3] == 1'b1) // Check if the next byte could be the start of a new message
                    next_state = BYTE_1;
                else
                    next_state = IDLE;
            end
        endcase
    end

    // Sequential logic for state transitions
    always @(posedge clk) begin
        if (reset)
            state <= IDLE;
        else
            state <= next_state;
    end
    
    assign done = done_reg;
endmodule
